# -*- coding: utf-8 -*-
from __future__ import absolute_import

from cchloader.backends import BaseBackend, register, urlparse
import datetime
import psycopg2
import pytz

def get_as_utc_timestamp(t):
    timezone_utc = pytz.timezone("UTC")
    timezone_local = pytz.timezone("Europe/Madrid")
    return timezone_utc.normalize(timezone_local.localize(t, is_dst=False))

def get_utc_timestamp_from_datetime_and_season(local_timestamp, season):
    """
    Returns UTC timestamp from local datetime and winter/summer flag
    :param local_timestamp: datetime (no localized)
    :param season:
    :return: datetime (UTC localized)
    """
    dst = season == 1 and True or False
    timezone_utc = pytz.utc
    timezone_local = pytz.timezone("Europe/Madrid")
    return (timezone_local.normalize(timezone_local.localize(local_timestamp, is_dst=dst))).astimezone(timezone_utc)

class TimescaleDBBackend(BaseBackend):
    """TimescaleDB Backend
    """
    collections = ['giscedata_corbagen']

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
        for collection in document.keys():
            if collection in self.collections:
                cch = document.get(collection)
                if cch:
                    cch.backend = self
                    cch.collection = collection
                    self.insert_cch(cch)

    def get_columns(self, collection):
        self.cr.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = %s", (collection, )
        )
        return [x[0] for x in self.cr.fetchall()]

    def insert_cch(self, cch):
        collection = cch.collection
        document = cch.backend_data

        columns = self.get_columns(collection)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # UTC timestamp used by GISCE
        if 'timestamp' in columns:
            utc_timestamp = get_utc_timestamp_from_datetime_and_season(document['local_timestamp'], document['season'])
            document['timestamp'] = utc_timestamp

        if 'created_at' in columns:
            document['created_at'] = timestamp

        if 'updated_at' in columns:
            document['updated_at'] = timestamp

        # UTC timestamp used by SOM
        if 'utc_timestamp' in columns:
            document['utc_timestamp'] = get_as_utc_timestamp(document['datetime'])

        if 'validated' in document and type(document['validated']) == bool:
            document['validated'] = 1 if document['validated'] else 0

        if 'datetime' in document and type(document['datetime']) == datetime.datetime:
            document['datetime'] = document['datetime'].strftime('%Y-%m-%d %H:%M:%S')

        if 'name' in document and type(document['name']) == type(u''):
            document['name'] = document['name'].encode('utf-8')

        placeholders = ', '.join(['%s'] * len(document))
        columns = ', '.join(document.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s ) RETURNING *" % (collection, columns, placeholders)
        self.cr.execute(sql, document.values())
        oid = self.cr.fetchone()[0]
        self.db.commit()
        return oid

    def get(self, collection, filters, fields=None):
        raise Exception("Not implemented cchloader.backend.timescale.get()")

    def disconnect(self):
        self.db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


register("timescale", TimescaleDBBackend)
