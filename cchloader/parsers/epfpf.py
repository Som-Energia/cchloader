from __future__ import absolute_import

from cchloader import logger
from cchloader.utils import build_dict
from cchloader.adapters.epfpf import EPFPFAdapter
from cchloader.models.epfpf import EPFPFSchema, tipomedida_valid
from cchloader.parsers.parser import Parser, register


class EPFPF(Parser):

    patterns = [
        # Documented
        '^EPFPF_(\w{2})_(\w{3})_(\w{4})_(\w{2})_(\d{8})\.(\d+)\.(\w{3})',
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
        parsed = {'epfpf': {}, 'orig': line}
        data = build_dict(self.headers, slinia)
        data['filename'] = filename
        result, errors = self.adapter.load(data)
        if errors:
            logger.error(errors)
        parsed['epfpf'] = result
        return parsed, errors


register(EPFPF)
