from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.reganecu import ReganecuAdapter
from cchloader.models.reganecu import ReganecuSchema
from cchloader.parsers.parser import Parser, register


class Reganecu(Parser):

    patterns = ['^([ABC])(\d{1})_reganecu_(\d{4})(\d{2})(\d{2})_']
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = ReganecuAdapter(strict=strict)
        self.schema = ReganecuSchema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields, key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = map(lambda s: s.strip(), slinia)
        parsed = {'reganecu': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['reganecu'] = result
        return parsed, errors


register(Reganecu)
