from cchloader.backends import BaseBackend, register, urlparse
from cchloader.compress import is_compressed_file
from collections import defaultdict, OrderedDict
import datetime
import psycopg2
import psycopg2.extras
import pytz

def get_as_utc_timestamp(t, cups, season=None):
    timezone_utc = pytz.timezone("UTC")
    timezone_local = pytz.timezone("Europe/Madrid")
    if cups[0:7] == 'ES00316' or cups[0:7] == 'ES04016':
        timezone_local = pytz.timezone("Atlantic/Canary")
    is_dst = season==1
    return timezone_utc.normalize(timezone_local.localize(t, is_dst=is_dst))


class TimescaleDBBackend(BaseBackend):
    """TimescaleDB Backend
    """
    batch_size = 500
    collection_prefix = 'tg_'
    collections = ['f1', 'p1', 'cchfact', 'cchval']

    def __init__(self, uri=None):
        if uri is None:
            uri = "timescale://localhost:5432/destral_db"
        super(TimescaleDBBackend, self).__init__(uri)

        self.uri = uri
        self.config = urlparse(self.uri)
        ts_con = " host=" + self.config['hostname'] + \
                " port=" + str(self.config['port']) + \
                " dbname=" + self.config['db'] + \
                " user=" + self.config['username'] + \
                " password=" + self.config['password']
        self.db = psycopg2.connect(ts_con)
        self.cr = self.db.cursor()


    def insert(self, document):
        self.insert_batch([document])

    def insert_batch(self, documents):
        batches_to_insert = defaultdict(list)
        for document in documents:
            for collection in self.collections:
                if collection in document:
                    cch = document.get(collection)
                    cch.backend = self
                    batches_to_insert[self.collection_prefix + collection].append(cch.backend_data)

        for collection, curves in batches_to_insert.items():
            self.insert_cch_batch(collection, curves)

    def insert_cch_batch(self, collection, curves):
        batch = []
        for curve in curves:
            curve.update({
                'create_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'create_uid': 1,
                'utc_timestamp': get_as_utc_timestamp(curve['datetime'], curve['name'], curve.get('season')).strftime('%Y-%m-%d %H:%M:%S')
            })

            if collection != "tg_cchval":
                if 'validated' not in curve:
                    curve['validated'] = 0
                curve['validated'] = int(curve['validated'])

            if 'datetime' in curve and type(curve['datetime']) == datetime.datetime:
                curve['datetime'] = curve['datetime'].strftime('%Y-%m-%d %H:%M:%S')

            if 'name' in curve and type(curve['name']) == type(u''):
                curve['name'] = curve['name'].encode('utf-8')

            # uses ordered dict to insert always in the same order
            batch.append(OrderedDict(sorted(curve.items())))
            if len(batch) >= self.batch_size:
                self.insert_cch_batch_chunk(collection, batch)
                batch = []
        if batch:
            self.insert_cch_batch_chunk(collection, batch)

    def insert_cch_batch_chunk(self, collection, batch):
        # in the same batch we can't have repeated items as postgresql on conflict will fail
        unique_batch = {item['name']+item['utc_timestamp']: item for item in batch}.values()

        field_names = unique_batch[0].keys()
        data = [vals.values() for vals in unique_batch]
        fields_to_update = []
        for field in field_names:
            if field in ['name', 'utc_timestamp', 'create_date', 'create_uid']:
                continue
            else:
                fields_to_update.append('{}=EXCLUDED.{}'.format(field, field))
        fields_to_update.append('write_date=EXCLUDED.create_date')
        fields_to_update.append('write_uid=EXCLUDED.create_uid')

        on_conflict = 'name, utc_timestamp'
        if collection == 'tg_p1':
            on_conflict = 'name, utc_timestamp, type'
        sql = "INSERT INTO {} ({}) VALUES %s ON CONFLICT ({}) DO UPDATE SET {};".format(
            collection,
            ','.join(field_names),
            on_conflict,
            ', '.join(fields_to_update)
        )

        psycopg2.extras.execute_values(self.cr, sql, data, template=None, page_size=9999)
        self.db.commit()

    def get(self, collection, filters, fields=None):
        raise Exception("Not implemented cchloader.backend.timescale.get()")

    def disconnect(self):
        self.db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


register("timescale", TimescaleDBBackend)
