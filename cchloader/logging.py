# -*- coding: utf-8 -*-
"""
    cchloader.logging
    ~~~~~~~~~~~~~~~

    Implements the logging support for SIPPERS

    You can use logging everywhere using::

        from cchloader import logger
        logger.info('Info message')
"""
from __future__ import absolute_import

import logging

try:
    import sentry_sdk
except ImportError:
    sentry_sdk = None
from raven import Client as SentryClient
from raven.handlers.logging import SentryHandler
from cchloader import VERSION

LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'


def setup_logging(level=None, logfile=None):
    """
    Setups cchloader logging system.

    It will setup sentry logging if SENTRY_DSN environment is defined

    :param level: logging.LEVEL to set to logger (defaults INFO)
    :param logfile: File to write the log
    :return: logger
    """
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter(LOG_FORMAT))

    logger = logging.getLogger('cchloader')
    del logger.handlers[:]
    logger.addHandler(stream)

    if logfile:
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter(LOG_FORMAT)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

    if sentry_sdk:
        sentry_sdk.init(release=VERSION)
    else:
        sentry = SentryClient()
        sentry.tags_context({'version': VERSION})
        sentry_handler = SentryHandler(sentry, level=logging.ERROR)
        logger.addHandler(sentry_handler)

    if isinstance(level, basestring):
        level = getattr(logging, level.upper(), None)

    if level is None:
        level = logging.INFO

    logger.setLevel(level)

    return logger
