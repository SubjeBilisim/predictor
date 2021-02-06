import os
from os import remove
from typing import Final
from unittest.mock import patch

from predictor.converter.intraday_dto_converter import IntradayDTOConverter
from predictor.main import Main
from predictor.utils.intraday_utils import IntradayUtils
from tests.base_test_case import BaseTestCase


class MainTestCase(BaseTestCase):
    PATH_CHECKPOINT_FILE: Final[str] = os.path.join('..', 'model', 'test_checkpoint.h5')
    PATH_MODEL_FILE: Final[str] = os.path.join('..', 'model', 'test.h5')
    PATH_MODEL_DIR: Final[str] = os.path.join('..', 'model')

    def tearDown(self):
        remove(self.PATH_CHECKPOINT_FILE)
        remove(self.PATH_MODEL_FILE)

    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_CHECKPOINT_FILE', new=PATH_CHECKPOINT_FILE)
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_MODEL_FILE', new=PATH_MODEL_FILE)
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_MODEL_DIR', new=PATH_MODEL_DIR)
    def test_predict(self):
        intraday_list = IntradayUtils.generate_test_data()
        frame = IntradayDTOConverter.to_dataframe(intraday_list)
        Main.fit(frame=frame, show_visualization=True)
        prediction = Main.predict(frame=frame, show_visualization=True)
        self.assertIsInstance(prediction.delta, float)
        self.assertGreater(prediction.delta, float('-2'))
        self.assertLess(prediction.delta, float('-1'))
        Main.plot_prediction(frame=frame)
