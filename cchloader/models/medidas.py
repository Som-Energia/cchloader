# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class MedidasSchema(Schema):
    cil = fields.String(position=0, required=True)
    datetime = fields.DateTime(position=1, format='%Y/%m/%d %H:%M:%S')
    season = fields.Integer(position=2, validate=OneOf([0, 1]))
    ae = fields.Integer(position=3, allow_none=True)
    r2 = fields.Integer(position=4, allow_none=True)
    r3 = fields.Integer(position=5, allow_none=True)
    factor_potencia = fields.Float(position=6, allow_none=True)
    tipo_factor_potencia = fields.Integer(position=7, allow_none=True)
    tipo_lectura = fields.String(position=8, validate=OneOf(['R', 'E']))


MedidasSchema()
