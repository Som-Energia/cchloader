from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.a5d import A5dAdapter
from cchloader.models.cch_autocons import CchAutoconsSchema
from cchloader.parsers.parser import Parser, register


class A5d(Parser):

    patterns = ['^A5D_(\d+)_(\d{4})_(\d{4})(\d{2})(\d{2})']
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = A5dAdapter(strict=strict)
        self.schema = CchAutoconsSchema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields, key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = map(lambda s: s.strip(), slinia)
        parsed = {'cch_autocons': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['cch_autocons'] = result
        return parsed, errors


register(A5d)
