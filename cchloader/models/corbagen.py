# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class CorbaGenSchema(Schema):
    name = fields.String(position=0, required=True)
    datetime = fields.DateTime(position=1, format='%Y-%m-%d %H:%M', required=True)
    season = fields.Integer(position=2, validate=OneOf([0, 1]), required=True)
    generacio = fields.Integer(position=3, required=True)
    autocons = fields.Integer(position=4, required=True)
    excedent = fields.Integer(position=5, required=True)

CorbaGenSchema()
