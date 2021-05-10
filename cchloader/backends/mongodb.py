from cchloader.backends import BaseBackend, register, urlparse
from cchloader.compress import is_compressed_file
import pymongo
import datetime

class MongoDBBackend(BaseBackend):
    """MongoDB Backend
    """
    collection_prefix = 'tg_'
    collections = ['cchfact', 'cchval', 'f1', 'p1', 'cch_gennetabeta', 'cch_autocons']

    def __init__(self, uri=None):
        if uri is None:
            uri = "mongodb://localhost:27017/somenergia"
        super(MongoDBBackend, self).__init__(uri)
        self.uri = uri
        self.config = urlparse(self.uri)
        self.connection = pymongo.MongoClient(self.uri)
        self.db = self.connection[self.config['db']]
        for collection in self.collections:
            collection = self.collection_prefix + collection
            self.db[collection].ensure_index(
                'name', background=True
            )

    def insert(self, document):
        for collection in document.keys():
            if collection in self.collections:
                cch = document.get(collection)
                if cch:
                    cch.backend = self
                    cch.collection = self.collection_prefix + collection
                    self.insert_cch(cch)

    def get(self, collection, filters, fields=None):
        return [x for x in self.db[collection].find(filters, fields=fields)]

    def insert_cch(self, cch):
        collection = cch.collection
        document = cch.backend_data
        document.update({
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        })
        oid = self.db[collection].insert(document)
        return oid

    def disconnect(self):
        self.connection.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


register("mongodb", MongoDBBackend)
