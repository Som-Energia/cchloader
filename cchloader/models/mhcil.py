# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class MhcilSchema(Schema):
    cil = fields.String(position=0, required=True)
    year = fields.Integer(position=1, required=True)
    month = fields.Integer(position=2, required=True)
    day = fields.Integer(position=3, required=True)
    hour = fields.Integer(position=4, required=True)
    season = fields.Integer(position=5, validate=OneOf([0, 1]))
    ae = fields.Float(position=6, allow_none=True)
    r2 = fields.Float(position=7, allow_none=True)
    r3 = fields.Float(position=8, allow_none=True)
    type_measure = fields.String(position=9, validate=OneOf(['R', 'E', 'L', 'M']))


MhcilSchema()
