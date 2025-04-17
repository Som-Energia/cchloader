# -*- coding: utf-8 -*-
from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.infpa import InfpaAdapter
from cchloader.models.infpa import InfpaSchema
from cchloader.parsers.parser import Parser, register
import six
if six.PY3:
    unicode = str



class Infpa(Parser):

    patterns = ['^INFPA_([H][23CPD])_(\d{4})_([PA][12])_(\d{4})(\d{2}).(\d)',
                '^INFPA_([H][23CPD])_(\d{4})_([PA][12])_(\d{4})(\d{2})']
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = InfpaAdapter(strict=strict)
        self.schema = InfpaSchema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields, key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = list(map(lambda s: s.strip(), slinia))
        parsed = {'infpa': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['infpa'] = result
        return parsed, errors


register(Infpa)
