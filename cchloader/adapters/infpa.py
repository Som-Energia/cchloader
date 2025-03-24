# -*- coding: utf-8 -*-
from __future__ import absolute_import

from cchloader.adapters import CchAdapter
from cchloader.models.infpa import InfpaSchema
from marshmallow import Schema, fields, pre_load


class InfpaBaseAdapter(Schema):
    """ INFPA Adapter
    """

    @pre_load
    def fix_numbers(self, data):
        for attr, field in self.fields.items():
            if isinstance(field, (fields.Integer, fields.Float)):
                if not data.get(attr):
                    data[attr] = None
        return data


class InfpaAdapter(InfpaBaseAdapter, CchAdapter, InfpaSchema):
    pass
