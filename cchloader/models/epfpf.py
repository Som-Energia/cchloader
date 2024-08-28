# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf

tipomedida_valid = [x for x in range(1,100)]

class EPFPFSchema(Schema):
    name = fields.String(position=0, required=True)
    year = fields.Integer(position=1)
    month = fields.Integer(position=2)
    day = fields.Integer(position=3)
    periodo = fields.Integer(position=4)
    magnitud = fields.String(position=5, validate=OneOf(['AE','AS','F1','F2','R1','R2','R3','R4']))
    valor = fields.Integer(position=6) # kWh
    firmeza = fields.String(position=7, validate=OneOf(['F','P']))
    cierre = fields.String(position=8, validate=OneOf(['P','D','']))
    tipo_medida = fields.Integer(position=9, validate=OneOf(tipomedida_valid))


EPFPFSchema()
