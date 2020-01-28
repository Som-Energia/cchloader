# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class P1Schema(Schema):

    valid_quality = range(0, 255)
    valid_activa_quality = range(0, 255)

    name = fields.String(position=0, required=True)
    measure_type = fields.Integer(position=1)  # hauria de ser sempre 11
    datetime = fields.DateTime(position=2, format='%Y/%m/%d %H:%M:%S')
    season = fields.Integer(position=3, validate=OneOf([0, 1]))
    ai = fields.Float(position=4)
    aiquality = fields.Integer(position=5, validate=OneOf(valid_activa_quality))
    ao = fields.Float(position=6, allow_none=True)
    aoquality = fields.Integer(position=7, allow_none=True,
                               validate=OneOf(valid_quality))
    r1 = fields.Float(position=8, allow_none=True)
    r1quality = fields.Integer(position=9, allow_none=True,
                               validate=OneOf(valid_quality))
    r2 = fields.Float(position=10, allow_none=True)
    r2quality = fields.Integer(position=11, allow_none=True,
                               validate=OneOf(valid_quality))
    r3 = fields.Float(position=12, allow_none=True)
    r3quality = fields.Integer(position=13, allow_none=True,
                               validate=OneOf(valid_quality))
    r4 = fields.Float(position=14, allow_none=True)
    r4quality = fields.Integer(position=15, allow_none=True,
                               validate=OneOf(valid_quality))
    reserve1 = fields.Float(position=16, allow_none=True)
    reserve1quality = fields.Integer(position=17, allow_none=True,
                                     validate=OneOf(valid_quality))
    reserve2 = fields.Float(position=18, allow_none=True)
    reserve2quality = fields.Integer(position=19, allow_none=True,
                                     validate=OneOf(valid_quality))
    source = fields.Integer(position=20,
                            allow_none=True,
                            validate=OneOf([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 22]),
                            )
    validated = fields.Boolean(position=21)
    type = fields.String(position=22, validate=OneOf(['p', 'p4']))


P1Schema()
