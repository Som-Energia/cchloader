# -*- coding: utf-8 -*-
from __future__ import absolute_import

from cchloader.adapters import CchAdapter
from cchloader.models.medidas import MedidasSchema
from marshmallow import Schema, fields, pre_load


class MedidasBaseAdapter(Schema):
    """ MEDIDAS Adapter
    """

    @pre_load
    def fix_numbers(self, data):
        for attr, field in self.fields.items():
            if isinstance(field, (fields.Integer, fields.Float)):
                if not data.get(attr):
                    data[attr] = None
        return data

    @pre_load
    def fix_ae(self, data):
        data['ae'] = data.get('ae', 0)

    @pre_load
    def fix_r2(self, data):
        data['r2'] = data.get('r2', 0)

    @pre_load
    def fix_r3(self, data):
        data['r3'] = data.get('r3', 0)

    @pre_load
    def fix_factor_potencia(self, data):
        factor_potencia = data.get('factor_potencia', 0.0)
        if ',' in factor_potencia:
            factor_potencia = factor_potencia.replace(',', '.')
        data['factor_potencia'] = factor_potencia

    @pre_load
    def fix_tipo_factor_potencia(self, data):
        data['tipo_factor_potencia'] = data.get('tipo_factor_potencia', 0)

    @pre_load
    def fix_season(self, data):
        valid_values = [0, 1]
        season = data.get('season')
        if season and season.isdigit() and season in map(str, valid_values):
            data['season'] = int(season)
        else:
            data['season'] = None


class MedidasAdapter(MedidasBaseAdapter, CchAdapter, MedidasSchema):
    pass
