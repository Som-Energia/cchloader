from cchloader.adapters import CchAdapter
from cchloader.models.p2 import P2Schema
from marshmallow import Schema, fields, pre_load


class P2BaseAdapter(Schema):
    """ P2 Adapter
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
    def valid_measure(self, data):
        ae_quality = data.get('ae_quality')
        r1_quality = data.get('r1_quality')
        r2_quality = data.get('r2_quality')
        r3_quality = data.get('r3_quality')
        r4_quality = data.get('r4_quality')
        reserve1_quality = data.get('reserve1_quality')
        reserve2_quality = data.get('reserve2_quality')

        ae_valid = 0
        if ae_quality < 128:
            ae_valid = 1
        r1_valid = 0
        if r1_quality < 128:
            r1_valid = 1
        r2_valid = 0
        if r2_quality < 128:
            r2_valid = 1
        r3_valid = 0
        if r3_quality < 128:
            r3_valid = 1
        r4_valid = 0
        if r4_quality < 128:
            r4_valid = 1
        res1_valid = 0
        if reserve1_quality < 128:
            res1_valid = 1
        res2_valid = 0
        if reserve2_quality < 128:
            res2_valid = 1

        data['ai_valid'] = 1
        data['ae_valid'] = ae_valid
        data['r1_valid'] = r1_valid
        data['r2_valid'] = r2_valid
        data['r3_valid'] = r3_valid
        data['r4_valid'] = r4_valid
        data['res1_valid'] = res1_valid
        data['res2_valid'] = res2_valid

        return data


class P2Adapter(P2BaseAdapter, CchAdapter, P2Schema):
    pass
