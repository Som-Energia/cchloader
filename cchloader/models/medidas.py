# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class MedidasSchema(Schema):
    cil = fields.String(position=0, required=True)
    year = fields.Integer(position=1, required=True)
    month = fields.Integer(position=2, required=True)
    day = fields.Integer(position=3, required=True)
    hour = fields.Integer(position=4, required=True)
    season = fields.Integer(position=5, validate=OneOf([0, 1]))
    ae = fields.Integer(position=6, allow_none=True)
    r2 = fields.Integer(position=7, allow_none=True)
    r3 = fields.Integer(position=8, allow_none=True)
    factor_potencia = fields.Float(position=8, allow_none=True)
    tipo_factor_potencia = fields.Integer(position=9, validate=OneOf([0, 1]))
    tipo_lectura = fields.String(position=9, validate=OneOf(['R', 'E']))


MedidasSchema()
