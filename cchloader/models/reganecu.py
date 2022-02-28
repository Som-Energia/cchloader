# -*- encoding: utf-8 -*-
from marshmallow import Schema, fields


class ReganecuSchema(Schema):
    date = fields.String(position=0, required=True)
    hour = fields.Integer(position=1, required=True)
    upr = fields.String(position=2, required=True)
    energia = fields.Float(position=3, required=True)
    reserved1 = fields.Integer(position=4)
    precio = fields.Float(position=5, required=True)
    reserved2 = fields.Integer(position=6)
    importe = fields.Float(position=7, required=True)
    reserved3 = fields.Integer(position=8)
    vendedor = fields.String(position=9, required=True)
    segmento = fields.String(position=10, required=True)
    facturacion = fields.Integer(position=11, required=True)
    eiec_upr = fields.String(position=12, required=True)
    cuenta = fields.String(position=13, required=True)
    signo_importe = fields.Integer(position=14, required=True)
    signo_magnitud = fields.Integer(position=15, required=True)
    eic_titular = fields.String(position=16, required=True)
    codigo_magnitud = fields.String(position=17, required=True)
    codigo_precio = fields.String(position=18, required=True)
    codigo_apunte = fields.String(position=19, required=True)
    tipo_oferta = fields.String(position=20, required=True)
    tipo_upr = fields.Integer(position=21, required=True)
    energia_bilateral = fields.Integer(position=22, required=True)
    sesion = fields.String(position=23, required=True)


ReganecuSchema()
