# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
import os
import re

from cchloader import logger
from cchloader.exceptions import ParserNotFoundException


_PARSERS = {

}


def register(cls):
    """Register a parser

    :type cls: Parser class
    """
    module = cls.__module__
    path = '.'.join([module, cls.__name__])
    _PARSERS[path] = cls


def get_parser(cch_file):
    for path, cls in _PARSERS.items():
        if cls.detect(cch_file):
            return cls
    logger.error("Parser not found for file %s", cch_file)
    raise ParserNotFoundException()


class Parser(object):
    """Base parser interface.
    """

    encoding = "iso-8859-15"

    @classmethod
    def detect(cls, cch_file):
        if cls.pattern:
            return re.match(cls.pattern, os.path.basename(cch_file))
        return False

    def parse_line(self, line):
        """Parse a line of a CCH file.

        :param line: line of the file
        """
        raise NotImplementedError("Should have implemented this")
