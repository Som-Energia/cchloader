from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.p2 import P2Adapter
from cchloader.models.p1 import P1Schema
from cchloader.parsers.parser import Parser, register


class P2D(Parser):

    patterns = ['^P2D_(\d{4})_(\d{4})_(\d{4})(\d{2})(\d{2}).(\d)']
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = P2Adapter(strict=strict)
        self.schema = P1Schema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields, key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = map(lambda s: s.strip(), slinia)
        parsed = {'p1': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['p1'] = result
        return parsed, errors


register(P2D)
