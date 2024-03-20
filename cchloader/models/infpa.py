# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from marshmallow import Schema, fields


class InfpaSchema(Schema):
    cil = fields.String(position=0, required=True)
    valor = fields.Integer(position=1, required=True)
    horas = fields.Integer(position=2, required=True)

InfpaSchema()
