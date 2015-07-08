from marshmallow import Schema, fields


class CchFactSchema(Schema):    
    name = fields.String(position=0)
    datetime = fields.DateTime(position=1, format='%Y/%m/%d %H:%M')
    season = fields.Select(position=2, choices=[0, 1])
    ai = fields.Integer(position=3)
    ao = fields.Integer(position=4, allow_none=True)
    r1 = fields.Integer(position=5, allow_none=True)
    r2 = fields.Integer(position=6, allow_none=True)
    r3 = fields.Integer(position=7, allow_none=True)
    r4 = fields.Integer(position=8, allow_none=True)
    source = fields.Select(position=9, choices=[1, 2, 3, 4, 5, 6])
    validated = fields.Boolean(position=10)
    bill = fields.String(position=11)
