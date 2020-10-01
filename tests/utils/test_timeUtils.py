import unittest
import datetime as dt
from src.utils.timeUtils import getWeekNumOfFinYr, getFinYearForDt, getSundayAfterDt, getMondayBeforeDt


class TestTimeUtils(unittest.TestCase):
    def test_weekNum(self) -> None:
        """tests the function that get the week number for a given input date
        """
        inpDt = dt.datetime(2020, 8, 10)
        weekNum = getWeekNumOfFinYr(inpDt)
        self.assertTrue(weekNum == 20)

    def test_finYr(self) -> None:
        """tests the function that get the financial year of input time
        """
        inpDt = dt.datetime(2020, 3, 31)
        finYr = getFinYearForDt(inpDt)
        self.assertTrue(finYr == 2020)

    def test_getFirstSundayAfterDate(self) -> None:
        """tests the function that gets the first Sunday after a date
        """
        inpDt = dt.datetime(2020, 10, 1)
        sundatDt = getSundayAfterDt(inpDt)
        self.assertTrue((sundatDt - dt.datetime(2020, 10, 4))
                        == dt.timedelta(days=0))

    def test_getFirstMondayBeforeDate(self) -> None:
        """tests the function that gets the first Monday before a date
        """
        inpDt = dt.datetime(2020, 10, 1)
        mondayDt = getMondayBeforeDt(inpDt)
        self.assertTrue((mondayDt - dt.datetime(2020, 9, 28))
                        == dt.timedelta(days=0))
