# -*- coding: utf-8 -*-
from __future__ import absolute_import

from cchloader.adapters import CchAdapter
from cchloader.models.mcilqh import McilQhSchema
from marshmallow import Schema, fields, pre_load


class McilQhBaseAdapter(Schema):
    """ MCILQH Adapter
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
        ae = int(data.get('ae', 0))
        if ae < 0:
            data['ae'] = 0

    @pre_load
    def fix_season(self, data):
        valid_values = [0, 1]
        season = data.get('season')
        if season and season.isdigit() and season in map(str, valid_values):
            data['season'] = int(season)
        else:
            data['season'] = None


class McilQhAdapter(McilQhBaseAdapter, CchAdapter, McilQhSchema):
    pass
