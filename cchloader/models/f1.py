# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class F1Schema(Schema):
    name = fields.String(position=0, required=True)
    measure_type = fields.Integer(position=1) # hauria de ser sempre 11
    datetime = fields.DateTime(position=2, format='%Y/%m/%d %H:%M:%S')
    season = fields.Integer(position=3, validate=OneOf([0, 1]))
    ai = fields.Integer(position=4)
    ao = fields.Integer(position=5, allow_none=True)
    r1 = fields.Integer(position=6, allow_none=True)
    r2 = fields.Integer(position=7, allow_none=True)
    r3 = fields.Integer(position=8, allow_none=True)
    r4 = fields.Integer(position=9, allow_none=True)
    reserve1 = fields.Integer(position=10, allow_none=True)
    reserve2 = fields.Integer(position=11, allow_none=True)
    source = fields.Integer(position=12,
                            validate=OneOf([1,2,3,4,5,6,7,8,9,10,11,22]))
    validated = fields.Boolean(position=13)

F1Schema()
