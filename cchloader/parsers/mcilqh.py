# -*- coding: utf-8 -*-
from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.mcilqh import McilQhAdapter
from cchloader.models.mcilqh import McilQhSchema
from cchloader.parsers.parser import Parser, register
import six
if six.PY3:
    unicode = str


class McilQh(Parser):

    patterns = ['^MCILQH_']
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = McilQhAdapter(strict=strict)
        self.schema = McilQhSchema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields, key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = list(map(lambda s: s.strip(), slinia))
        parsed = {'mcilqh': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['mcilqh'] = result
        return parsed, errors


register(McilQh)
