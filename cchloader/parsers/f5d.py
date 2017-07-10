from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.f5d import F5dAdapter
from cchloader.models.cchfact import CchFactSchema
from cchloader.parsers.parser import Parser, register


class F5d(Parser):

    patterns = ['^F5D_(\d+)_(\d{4})_(\d{4})(\d{2})(\d{2})']
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter =F5dAdapter(strict=strict)
        self.schema = CchFactSchema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields,
                key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = map(lambda s: s.strip(), slinia)
        parsed = {'cchfact': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['cchfact'] = result
        return parsed, errors


register(F5d)
