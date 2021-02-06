import os
from decimal import Decimal
from os.path import exists
from typing import Final
from unittest.mock import patch

from predictor.utils.intraday_utils import IntradayUtils
from tests.base_test_case import BaseTestCase


class IntradayUtilsTestCase(BaseTestCase):
    CSV_PATH: Final[str] = os.path.join('..', '..', '..', 'data', 'test_symbol{}_year{}_month{}.csv')

    def tearDown(self):
        for year in range(IntradayUtils.YEAR_RANGE):
            for month in range(IntradayUtils.MONTH_RANGE):
                path = self.CSV_PATH.format('IBM', year + 1, month + 1)
                if exists(path):
                    os.remove(path)

    @patch('predictor.utils.intraday_utils.IntradayUtils.CSV_PATH', new=CSV_PATH)
    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday_extended')
    def test_write_time_series_intraday_extended(self, csv):
        expected_list = self.create_intraday_list(tuple('IBM' for _ in range(10)))
        csv_list = [['time', 'open', 'high', 'low', 'close', 'volume']]
        for expected in expected_list:
            csv_list.append([str(expected.date), str(expected.open), str(expected.high), str(expected.low),
                             str(expected.close), str(expected.volume)])
        csv.return_value = csv_list, None
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayUtils.write_time_series_intraday_extended()
        actual_list = IntradayUtils.read_time_series_intraday_extended()
        for actual, expected in zip(actual_list, expected_list):
            self.assert_intraday(actual, expected, Decimal)
