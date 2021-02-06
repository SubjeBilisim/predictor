from unittest import TestCase

from predictor.utils.utils import Utils


class UtilsTestCase(TestCase):

    def test_is_test(self):
        self.assertTrue(Utils.is_test())
