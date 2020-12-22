from datetime import datetime
from decimal import Decimal
from typing import Type, Union, Final, Tuple
from unittest import TestCase

from pandas import date_range

from predictor.dto.intraday_dto import IntradayDTO


class BaseTestCase(TestCase):
    TICKER_LIST: Final[Tuple[str]] = ('AAA', 'AAA', 'AAA', 'AAA', 'BBB', 'BBB', 'CCC', 'DDD', 'DDD', 'DDD')

    @staticmethod
    def create_intraday_list(symbol_list: Tuple[str] = TICKER_LIST):
        intraday_list = []
        decimal_list = [Decimal(i) for i in range(len(symbol_list))]
        dates = date_range(end='2020-02-02', periods=10).to_pydatetime().tolist()
        for date, symbol, decimal in zip(dates, symbol_list, decimal_list):
            intraday_list.append(IntradayDTO(date, decimal, decimal, decimal, decimal, decimal, symbol))
        return intraday_list

    def assert_intraday(self, actual: IntradayDTO, expected: IntradayDTO, decimal: Type[Union[Decimal, float]]):
        self.assertIsInstance(actual.date, datetime)
        self.assertIsInstance(actual.open, decimal)
        self.assertIsInstance(actual.high, decimal)
        self.assertIsInstance(actual.low, decimal)
        self.assertIsInstance(actual.close, decimal)
        self.assertIsInstance(actual.volume, decimal)
        self.assertIsInstance(actual.symbol, str)

        self.assertEqual(actual.date, expected.date)
        self.assertEqual(actual.open, expected.open)
        self.assertEqual(actual.high, expected.high)
        self.assertEqual(actual.low, expected.low)
        self.assertEqual(actual.close, expected.close)
        self.assertEqual(actual.volume, expected.volume)
        self.assertEqual(actual.symbol, expected.symbol)
