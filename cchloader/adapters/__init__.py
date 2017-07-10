from marshmallow import Schema, post_load
from marshmallow.decorators import tag_processor
from cchloader.models import Document


def pre_insert(fn=None, raw=False):
    """Filter to use before inserting the document to the database.

    Useful when you must to do some operation between the parsed data and the
    already inserted data.
    """
    return tag_processor('pre_insert', fn, raw)


class CchAdapter(Schema):
    """Base Cch Adapter.
    """

    @post_load
    def make_object(self, data):
        return Document(data, adapter=self)
