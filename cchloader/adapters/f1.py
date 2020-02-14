from cchloader.adapters import CchAdapter
from cchloader.models.f1 import F1Schema
from marshmallow import Schema, fields, pre_load

class F1BaseAdapter(Schema):
    """ F1 Adapter
    """

    @pre_load
    def fix_numbers(self, data):
        for attr, field in self.fields.iteritems():
            if isinstance(field, (fields.Integer, fields.Float)):
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

    @pre_load
    def fix_source(self, data):
        valid_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 22]
        source = data.get('source')
        if source and source.isdigit() and int(source) in valid_values:
            data['source'] = int(source)
        else:
            data['source'] = None

class F1Adapter(F1BaseAdapter, CchAdapter, F1Schema):
    pass
