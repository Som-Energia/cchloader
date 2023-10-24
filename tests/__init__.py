#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from pytz import timezone

class CchloaderBackendTimescaleTest(unittest.TestCase):

    def test__get_as_utc_timestamp__peninsula(self):
        from cchloader.backends.timescaledb import get_as_utc_timestamp

        result_winter = get_as_utc_timestamp(datetime(2023,1,1), 'ES123456748798', 0)
        result_summer = get_as_utc_timestamp(datetime(2023,10,1), 'ES123456748798', 1)

        self.assertEqual(datetime(2022, 12, 31, 23, 0, tzinfo=timezone('utc')), result_winter)
        self.assertEqual(datetime(2023, 9, 30, 22, 0, tzinfo=timezone('utc')), result_summer)

    def test__get_as_utc_timestamp__canary_islands(self):
        from cchloader.backends.timescaledb import get_as_utc_timestamp

        result_winter = get_as_utc_timestamp(datetime(2023,1,1), 'ES0031656748798', 0)
        result_summer = get_as_utc_timestamp(datetime(2023,10,2), 'ES0031656748798', 1)

        self.assertEqual(datetime(2023, 1, 1, 0, 0, tzinfo=timezone('utc')), result_winter)
        self.assertEqual(datetime(2023, 10, 1, 23, 0, tzinfo=timezone('utc')), result_summer)

if __name__ == '__main__':
    unittest.main()

