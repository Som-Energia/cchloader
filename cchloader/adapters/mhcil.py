from cchloader.adapters import CchAdapter
from cchloader.models.mhcil import MhcilSchema
from marshmallow import Schema, fields, pre_load


class MhcilBaseAdapter(Schema):
    """ MHCIL Adapter
    """

    @pre_load
    def fix_numbers(self, data):
        for attr, field in self.fields.iteritems():
            if isinstance(field, (fields.Integer, fields.Float)):
                if not data.get(attr):
                    data[attr] = None
        return data

    @pre_load
    def fix_ae(self, data):
        ae = data.get('ae', 0)
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


class MhcilAdapter(MhcilBaseAdapter, CchAdapter, MhcilSchema):
    pass
