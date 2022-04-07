from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.f1 import F1Adapter
from cchloader.models.f1 import F1Schema
from cchloader.parsers.parser import Parser, register


class F1(Parser):

    patterns = [
        # Documented
        '^F1_(\d{4})_(\d{4})(\d{2})(\d{2})_(\d{4})(\d{2})(\d{2}).(\d)',
        # Fenosa
        '^F1_(\d{4})_(\d{4})_(\d{4})(\d{2})(\d{2})_(\d{4})(\d{2})(\d{2}).(\d)',
        # Endesa
        '^F1_(\d{4})_(\d{4})(\d{2})(\d{2}).(\d)',
        # Viesgo
        '^(\d{4})_F1_(\d{4})_(\d{4})(\d{2})(\d{2})_(\d{4})(\d{2})(\d{2}).(\d)',
    ]
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = F1Adapter(strict=strict)
        self.schema = F1Schema(strict=strict)
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
        parsed = {'f1': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:

            logger.error(errors)
        parsed['f1'] = result
        return parsed, errors

register(F1)
