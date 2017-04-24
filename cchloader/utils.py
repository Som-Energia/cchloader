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


def get_curve_cups(cups_name):
    """
    Gets cups to search curve by cups. Some DFO's change termination in
    x5D files (i,e, FENOSA puts 1F instead of 1P)
    """
    if len(cups_name) == 22 and cups_name[-2:] == '1P':
        cups = cups_name[:20]
        return cups + '1F'
    else:
        return cups_name
