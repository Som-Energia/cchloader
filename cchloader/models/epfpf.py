# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf

tipomedida_valid = [1,2,3,4,5,7,8,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,37,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,73,75,76,78,79,80,82,83,84,87,88,89,90,91,92,93,94,95,96,97,98,99,]

class EPFPFSchema(Schema):
    name = fields.String(position=0, required=True)
    year = fields.Integer(position=1)
    month = fields.Integer(position=2)
    day = fields.Integer(position=3)
    periodo = fields.Integer(position=4)
    magnitud = fields.String(position=5, validate=OneOf(['AE','AS','F1','F2','R1','R2','R3','R4']))
    valor = fields.Integer(position=6)
    firmeza = fields.String(position=7, validate=OneOf(['F','P']))
    cierre = fields.String(position=8, validate=OneOf(['P','D','']))
    tipo_medida = fields.Integer(position=9, validate=OneOf(tipomedida_valid))
    validated = fields.Boolean(position=10)
    date = fields.Date(position=11)
    filename = fields.String(position=12)

EPFPFSchema()
