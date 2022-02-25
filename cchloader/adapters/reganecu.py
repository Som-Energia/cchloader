from cchloader.adapters import CchAdapter
from cchloader.models.reganecu import ReganecuSchema
from marshmallow import Schema, fields, pre_load


class ReganecuBaseAdapter(Schema):
    """ REGANECU Adapter
    """

    @pre_load
    def fix_numbers(self, data):
        for attr, field in self.fields.iteritems():
            if isinstance(field, (fields.Integer, fields.Float)):
                if not data.get(attr):
                    data[attr] = None
        return data


class ReganecuAdapter(ReganecuBaseAdapter, CchAdapter, ReganecuSchema):
    pass
