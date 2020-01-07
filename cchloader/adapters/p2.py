from cchloader.adapters import CchAdapter
from cchloader.adapters.p1 import P1BaseAdapter
from cchloader.models.p1 import P1Schema
from marshmallow import pre_load


class P2BaseAdapter(P1BaseAdapter):

    @pre_load
    def fix_type(self, data):
        source = data.get('type')
        if not source:
            data['type'] = 'p4'


class P2Adapter(P2BaseAdapter, CchAdapter, P1Schema):
    pass
