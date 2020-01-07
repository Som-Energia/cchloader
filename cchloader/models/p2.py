# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class P2Schema(Schema):

    valid_quality = range(0, 255)
    valid_activa_quality = range(0, 255)

    name = fields.String(position=0, required=True)  # 8*c
    measure_type = fields.Integer(position=1)  # 2*n  [8: Absoluta, 11: Incremental]  # should be always 11
    datetime = fields.DateTime(position=2, format='%Y/%m/%d %H:%M:%S')  # aaaa/mm/dd hh:mm:ss
    season = fields.Integer(position=3, validate=OneOf([0, 1]))  # 1*c  [0: Invierno, 1: Verano]
    ai = fields.Float(position=4)  # 10*n
    ai_quality = fields.Integer(position=5, validate=OneOf(valid_activa_quality))  # 3*n
    ae = fields.Float(position=6, allow_none=True)  # 10*n
    ae_quality = fields.Integer(position=7, allow_none=True, validate=OneOf(valid_quality))  # 3*n
    r1 = fields.Float(position=8, allow_none=True)  # 10*n
    r1_quality = fields.Integer(position=9, allow_none=True, validate=OneOf(valid_quality))  # 3*n
    r2 = fields.Float(position=10, allow_none=True)  # 10*n
    r2_quality = fields.Integer(position=11, allow_none=True, validate=OneOf(valid_quality))  # 3*n
    r3 = fields.Float(position=12, allow_none=True)  # 10*n
    r3_quality = fields.Integer(position=13, allow_none=True, validate=OneOf(valid_quality))  # 3*n
    r4 = fields.Float(position=14, allow_none=True)  # 10*n
    r4_quality = fields.Integer(position=15, allow_none=True, validate=OneOf(valid_quality))  # 3*n
    reserve1 = fields.Integer(position=16, allow_none=True)  # 10*n
    reserve1_quality = fields.Integer(position=17, allow_none=True, validate=OneOf(valid_quality))  # 3*n
    reserve2 = fields.Integer(position=18, allow_none=True)  # 10*n
    reserve2_quality = fields.Integer(position=19, allow_none=True, validate=OneOf(valid_quality))  # 3*n
    source = fields.Integer(position=20, allow_none=True,
                            validate=OneOf([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 22]))  # 2*n
    validated = fields.Boolean(position=21)  # 1*n  [0: No firme, 1: Firme]


P2Schema()
