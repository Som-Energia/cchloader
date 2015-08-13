from cchloader.adapters import CchAdapter
from cchloader.models.cchval import CchValSchema
from marshmallow import Schema, fields, pre_load


class P5dBaseAdapter(Schema):
    """ P5D Adapter
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


class P5dAdapter(P5dBaseAdapter, CchAdapter, CchValSchema):
    pass
