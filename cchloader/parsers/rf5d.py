from __future__ import absolute_import

from cchloader.parsers import F5d
from cchloader.parsers.parser import register


class Rf5d(F5d):

    patterns = ['^RF5D_(\d+)_(\d{4})_(\d{4})(\d{2})(\d{2})']


register(Rf5d)
