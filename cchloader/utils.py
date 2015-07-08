#!/usr/bin/env python
# -*- coding: utf-8 -*-

def build_dict(headers, data):
    """Build a dict with headers and list of data.

    Example::

        build_dict(['foo', 'bar'], [1, 2])
        {'foo': 1, 'bar': 2}

    :param list headers: List of headers
    :param list data: List of data
    """
    return dict(zip(headers, data))
