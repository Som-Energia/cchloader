# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class CchAutoconsSchema(Schema):
    name = fields.String(position=0, required=True)
    datetime = fields.DateTime(position=1, format='%Y/%m/%d %H:%M')
    season = fields.Integer(position=2, validate=OneOf([0, 1]))
    ai = fields.Integer(position=3)
    ae = fields.Integer(position=4, allow_none=True)
    r1 = fields.Integer(position=5, allow_none=True)
    r2 = fields.Integer(position=6, allow_none=True)
    r3 = fields.Integer(position=7, allow_none=True)
    r4 = fields.Integer(position=8, allow_none=True)
    source = fields.Integer(position=9, validate=OneOf([1, 2, 3, 4, 5, 6]), allow_none=True)
    validated = fields.String(position=10, default='')
    bill = fields.String(position=11)


CchAutoconsSchema()
