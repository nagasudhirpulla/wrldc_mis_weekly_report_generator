import unittest
import datetime as dt
from src.utils.stringUtils import removeRedundantRemarks, combineTagReasonRemarks


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

        tag, reas, rem = removeRedundantRemarks(
            "Voltage Regulation", " VR", "vr")
        self.assertTrue((tag == "Voltage Regulation") and (
            reas == None) and (rem == None))

        tag, reas, rem = removeRedundantRemarks(
            "Manually opened due to High Voltage", " mohv", "MoHV")
        self.assertTrue((tag == "Manually opened due to High Voltage") and (
            reas == None) and (rem == None))

        tag, reas, rem = removeRedundantRemarks(
            "Voltage Regulation", " VR", "vr. ")
        self.assertTrue((tag == "Voltage Regulation") and (
            reas == None) and (rem == None))

        tag, reas, rem = removeRedundantRemarks(
            "Manually opened due to High Voltage", " Vr.", "VR")
        self.assertTrue((tag == "Manually opened due to High Voltage") and (
            reas == None) and (rem == None))

        tag, reas, rem = removeRedundantRemarks("RSD", "rsd", "rsd.")
        self.assertTrue((tag == "RSD") and (
            reas == None) and (rem == None))

    def test_combineTagReasonRemarks(self) -> None:
        """tests the function that combines tag, reason, remarks
        """
        self.assertTrue(combineTagReasonRemarks(
            "abcd", "rdf", "xyz") == "abcd / rdf / xyz")

        self.assertTrue(combineTagReasonRemarks(
            "RSD", None, "") == "RSD")

        self.assertTrue(combineTagReasonRemarks(
            "RSD", None, None) == "RSD")

        self.assertTrue(combineTagReasonRemarks(
            "RSD", "adsd", None) == "RSD / adsd")
