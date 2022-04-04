from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.mhcil import MhcilAdapter
from cchloader.models.mhcil import MhcilSchema
from cchloader.parsers.parser import Parser, register


class Mhcil(Parser):

    patterns = ['^MHCIL_([H][23CP])_(\d{4})_([PA][12])_(\d{4})(\d{2})(\d{2}).(\d)',
                '^MHCIL_([H][23CP])_(\d{4})_([PA][12])_(\d{4})(\d{2})(\d{2})']
    encoding = "iso-8859-15"
    delimiter = ';'

    def __init__(self, strict=False):
        self.adapter = MhcilAdapter(strict=strict)
        self.schema = MhcilSchema(strict=strict)
        self.fields = []
        self.headers = []
        for f in sorted(self.schema.fields, key=lambda f: self.schema.fields[f].metadata['position']):
            field = self.schema.fields[f]
            self.fields.append((f, field.metadata))
            self.headers.append(f)

    def parse_line(self, line):
        slinia = tuple(unicode(line.decode(self.encoding)).split(self.delimiter))
        slinia = map(lambda s: s.strip(), slinia)
        parsed = {'mhcil': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['mhcil'] = result
        return parsed, errors


register(Mhcil)
