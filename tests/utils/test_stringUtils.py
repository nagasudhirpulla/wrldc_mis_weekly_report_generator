import unittest
import datetime as dt
from src.utils.stringUtils import removeRedundantRemarks


class TestStringUtils(unittest.TestCase):
    def test_removeRedundantRemarks(self) -> None:
        """tests the function that removes redundant remarks
        """
        tag, reas, rem = removeRedundantRemarks("Outage", "RSD", "RSD")
        self.assertTrue((tag == None) and (reas == "RSD") and (rem == "RSD"))

        tag, reas, rem = removeRedundantRemarks("RSD", "RSD ", " rsd")
        self.assertTrue((tag == "RSD") and (reas == None) and (rem == None))

        tag, reas, rem = removeRedundantRemarks("RSD", "something", " rsd")
        self.assertTrue((tag == "RSD") and (
            reas == "something") and (rem == None))

        tag, reas, rem = removeRedundantRemarks("RSD", " rsd", "somthing")
        self.assertTrue((tag == "RSD") and (
            reas == None) and (rem == "somthing"))
