# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.epfpf import EPFPFAdapter
from cchloader.models.epfpf import EPFPFSchema
from cchloader.parsers.parser import Parser, register
from datetime import datetime, timedelta
from pytz import timezone

import six
if six.PY3:
    unicode = str

class EPFPF(Parser):

    patterns = [
        # Documented
        '^EPFPF_(\w{2})_(\w{3})_(\w{4})_(\w{2})_(\d{8})\.(\d+)',
    ]
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = EPFPFAdapter(strict=strict)
        self.schema = EPFPFSchema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields,
                key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line, filename = None):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = map(lambda s: s.strip(), slinia)
        parsed = {'giscedata_epfpf': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        data['filename'] = filename
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)

        # Add local_timestamp and season fields
        dt, season = self.get_datetime_and_season(result.data)
        result.data['local_timestamp'] = dt
        result.data['season'] = season

        # Add type 'p'
        result.data['type'] = 'p'

        # Remove unused fields
        for field in ['year', 'month', 'day', 'periodo']:
            if field in result.data:
                result.data.pop(field)

        # Convert to regular curve (using ai, ae, r1, r2, r3, r4 magns instead of magnitud, valor)
        result.data = self.get_magn(result.data)

        parsed['giscedata_epfpf'] = result
        return parsed, errors

    def get_datetime_and_season(self, data):
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))
        periodo = int(data.get('periodo'))
        dt = datetime(year=year, month=month, day=day)
        mad_tz = timezone('Europe/Madrid')
        local_datetime = mad_tz.localize(dt, is_dst=None)
        hours = timedelta(hours=periodo)
        final_date = mad_tz.normalize(local_datetime + hours)
        dt = final_date.strftime('%Y-%m-%d %H:%M:%S')
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        season = 1 if final_date.dst().total_seconds() == 3600 else 0
        return dt, season

    def get_magn(self, data):
        magn = data.get('magnitud').lower()
        data[magn] = data.get('valor')
        for field in ['magnitud', 'valor']:
            data.pop(field, False)
        return data


register(EPFPF)