# -*- coding: utf-8 -*-
from __future__ import absolute_import

from cchloader.adapters import CchAdapter
from cchloader.models.reganecuqh import ReganecuQhSchema
from marshmallow import Schema, fields, pre_load


class ReganecuQhBaseAdapter(Schema):
    """ REGANECUQh Adapter
    """

    @pre_load
    def fix_numbers(self, data):
        for attr, field in self.fields.items():
            if isinstance(field, (fields.Integer, fields.Float)):
                if not data.get(attr):
                    data[attr] = None
        return data


class ReganecuQhAdapter(ReganecuQhBaseAdapter, CchAdapter, ReganecuQhSchema):
    pass
