from cchloader.adapters import CchAdapter
from cchloader.models.epfpf import EPFPFSchema
from marshmallow import Schema, fields, pre_load

class EPFPFBaseAdapter(Schema):
    """ EPFPF Adapter
    """

    @pre_load
    def fix_date(self, data):
        year = data.get('any')
        month = data.get('mes')
        day = data.get('dia')
        if year and month and day:
            data['date'] = year + '-' + month + '-' + day

    @pre_load
    def fix_date(self, data):
        cierre = data.get('cierre')
        if not cierre:
            data['cierre'] = ''

    @pre_load
    def set_default_validated(self, data):
        data['validated'] = False

class EPFPFAdapter(EPFPFBaseAdapter, CchAdapter, EPFPFSchema):
    pass
