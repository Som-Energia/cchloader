from datetime import datetime, timedelta
from pytz import timezone
from cchloader.adapters import CchAdapter
from cchloader.models.epfpf import EPFPFSchema
from marshmallow import Schema, fields, pre_load

class EPFPFBaseAdapter(Schema):
    """ EPFPF Adapter
    """

    @pre_load
    def fix_date(self, data):
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))
        periodo = int(data.get('periodo'))
        dt = datetime(year=year, month=month, day=day)
        mad_tz = timezone('Europe/Madrid')
        local_datetime = mad_tz.localize(dt, is_dst=None)
        hours = timedelta(hours=periodo)
        final_date = mad_tz.normalize(local_datetime + hours)
        data['datetime'] = final_date.strftime('%Y-%m-%d %H:%M:%S')
        data['season'] = 'S' if final_date.dst().total_seconds() == 3600 else 'W'

    @pre_load
    def fix_cierre(self, data):
        cierre = data.get('cierre')
        if not cierre:
            data['cierre'] = ''

    @pre_load
    def set_default_validated(self, data):
        data['validated'] = False

class EPFPFAdapter(EPFPFBaseAdapter, CchAdapter, EPFPFSchema):
    pass
