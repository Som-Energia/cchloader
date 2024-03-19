# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from cchloader.adapters import CchAdapter
from cchloader.models.corbagen import CorbaGenSchema
from marshmallow import Schema, fields, pre_load


class CorbaGenBaseAdapter(Schema):
    """ CORBAGEN Adapter
    """

    @pre_load
    def fix_numbers(self, data):
        for attr, field in self.fields.iteritems():
            if isinstance(field, fields.Integer):
                if not data.get(attr):
                    data[attr] = None
        return data

    @pre_load
    def fix_season(self, data):
        valid_values = [0, 1]
        season = data.get('season')
        if season and season.isdigit() and season in map(str, valid_values):
            data['season'] = int(season)
        else:
            data['season'] = None


class CorbaGenAdapter(CorbaGenBaseAdapter, CchAdapter, CorbaGenSchema):
    pass
