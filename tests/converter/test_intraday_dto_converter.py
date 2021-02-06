from decimal import Decimal
from os import remove

from src.predictor.converter.intraday_dto_converter import IntradayDTOConverter
from tests.base_test_case import BaseTestCase


class IntradayDTOConverterTestCase(BaseTestCase):
    INTRADAY_LIST = BaseTestCase.create_intraday_list(tuple('AAA' for _ in range(10)))
    CSV_FILE = 'file.csv'
    JSON_FILE = 'file.json'

    def setUp(self):
        IntradayDTOConverter.to_csv(self.INTRADAY_LIST, open(self.CSV_FILE, 'a'))
        self.__create_file()

    def tearDown(self):
        remove(self.CSV_FILE)
        remove(self.JSON_FILE)

    def test_from_json(self):
        json_file = open(self.JSON_FILE, 'r')
        intraday_list = IntradayDTOConverter.from_json(json_file.read())
        self.assertEqual(len(intraday_list), 10)
        for actual, expected in zip(intraday_list, self.create_intraday_list()):
            self.assert_intraday(actual, expected, Decimal)

    def test_to_dataframe(self):
        json_file = open(self.JSON_FILE, 'r')
        intraday_list = IntradayDTOConverter.from_json(json_file.read())
        frame = IntradayDTOConverter.to_dataframe(intraday_list)
        self.assertEqual(frame.shape[0], 10)
        for i in range(frame.shape[0]):
            self.assert_intraday(frame.iloc[i], self.create_intraday_list()[i], float)

    def test_group_by_symbol(self):
        intraday_list = self.create_intraday_list()
        symbol_list = set(map(lambda item: item.symbol, intraday_list))
        grouped = IntradayDTOConverter.group_by_symbol(intraday_list)
        for group, symbol in zip(grouped, symbol_list):
            for intraday in group:
                self.assertEqual(symbol, intraday.symbol)

    def test_from_csv(self):
        actual_list = IntradayDTOConverter.from_csv(open(self.CSV_FILE, 'r'), 'AAA')
        for actual, expected in zip(actual_list, self.INTRADAY_LIST):
            self.assert_intraday(actual, expected, Decimal)

    @classmethod
    def __create_file(cls):
        json_file = open(cls.JSON_FILE, 'a')
        json_file.write(IntradayDTOConverter.to_json(cls.create_intraday_list()))
        json_file.close()
