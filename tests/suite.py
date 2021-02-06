from unittest import TestLoader, TextTestRunner

suite = TestLoader().discover('..')
runner = TextTestRunner()
runner.run(suite)
