# -*- coding: utf-8 -*-
class Pymongo:
    @staticmethod
    def monkeypatch():
        print('Applying monkeypatch for Pymongo')
        from pymongo.mongo_client import MongoClient
        from pymongo.command_cursor import CommandCursor
        from pymongo.collection import Collection

        if not hasattr(MongoClient, 'disconnect'):
            MongoClient.disconnect = MongoClient.close

        def patch_getitem(self, item):
            if item == 'result':
                # return self
                return [_rec for _rec in self]
            raise TypeError("'CommandCursor' object has no attribute '__getitem__'")

        CommandCursor.__getitem__ = patch_getitem

        original_aggregate = Collection.aggregate

        def patch_aggregate(self, *args, **kwargs):
            if 'cursor' not in kwargs.keys():
                kwargs['cursor'] = {}
            return original_aggregate(self, *args, **kwargs)

        Collection.aggregate = patch_aggregate
