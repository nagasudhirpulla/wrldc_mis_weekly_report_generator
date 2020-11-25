import unittest
import datetime as dt
from src.config.appConfig import getConfig
from src.appLogger import initAppLogger


class TestAppLogger(unittest.TestCase):
    def test_run(self) -> None:
        """tests the function that Logs data
        """
        appConfig = getConfig()
        appLogger = initAppLogger(appConfig)
        appLogger.info("test logging", extra={"ctx": "testing"})
        self.assertTrue(True)
