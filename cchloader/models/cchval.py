# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class CchValSchema(Schema):
    name = fields.String(position=0, required=True)
    datetime = fields.DateTime(position=1, format='%Y/%m/%d %H:%M')
    season = fields.Integer(position=2, validate=OneOf([0, 1]))
    ai = fields.Integer(position=3)
    ao = fields.Integer(position=4, allow_none=True)

CchValSchema()
