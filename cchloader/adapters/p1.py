from cchloader.adapters import CchAdapter
from cchloader.models.p1 import P1Schema
from marshmallow import Schema, fields, pre_load


class P1BaseAdapter(Schema):
    """ P1 Adapter
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

    @pre_load
    def fix_validated(self, data):
        source = data.get('validated')
        if not source:
            data['validated'] = 0

    @pre_load
    def fix_type(self, data):
        source = data.get('type')
        if not source:
            data['type'] = 'p'

    @pre_load
    def valid_measure(self, data):
        aoquality = data.get('aoquality')
        r1quality = data.get('r1quality')
        r2quality = data.get('r2quality')
        r3quality = data.get('r3quality')
        r4quality = data.get('r4quality')
        reserve1quality = data.get('reserve1quality')
        reserve2quality = data.get('reserve2quality')

        aovalid = 0
        if aoquality < 128:
            aovalid = 1
        r1valid = 0
        if r1quality < 128:
            r1valid = 1
        r2valid = 0
        if r2quality < 128:
            r2valid = 1
        r3valid = 0
        if r3quality < 128:
            r3valid = 1
        r4valid = 0
        if r4quality < 128:
            r4valid = 1
        res1valid = 0
        if reserve1quality < 128:
            res1valid = 1
        res2valid = 0
        if reserve2quality < 128:
            res2valid = 1

        data['aivalid'] = 1
        data['aovalid'] = aovalid
        data['r1valid'] = r1valid
        data['r2valid'] = r2valid
        data['r3valid'] = r3valid
        data['r4valid'] = r4valid
        data['res1valid'] = res1valid
        data['res2valid'] = res2valid

        return data


class P1Adapter(P1BaseAdapter, CchAdapter, P1Schema):
    pass
