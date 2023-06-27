from __future__ import absolute_import
import traceback


class BaseBackend(object):
    """Base backend interface

    :param uri: URI to get the properties for the backend.
    """
    def __init__(self, uri):
        pass

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    def insert(self, document):
        raise NotImplementedError()

    def insert_batch(self, documents):
        """ This method returns the errors in a list of strings with it's trace
        """
        errors = []
        for document in documents:
            try:
                self.insert(document)
            except Exception as _:
                errors.append(traceback.format_exc())
        return errors

    def get(self, collection, filters, fields=None):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()
