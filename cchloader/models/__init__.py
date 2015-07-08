from marshmallow import Schema, fields


class Document(object):
    """Document object

    :param data: Data parsed.
    :param adapter: Adapter used to parse this data.

    This document is used to encapsulated a object in
    :func:`cchloader.parsers.parser.Parser.parse_line`
    """
    def __init__(self, data, adapter):
        self.data = data
        self.adapter = adapter
        self.backend = None

    @property
    def backend_data(self):
        """Get data after using the filter :func:`cchloader.adapters.pre_insert`
        """
        if not self.backend:
            raise Exception("No backend defined")
        self.adapter.backend = self.backend
        return self.adapter._invoke_processors(
            'pre_insert', False, self.data, False
        )
