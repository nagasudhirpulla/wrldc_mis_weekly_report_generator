import datetime as dt


def getWeekNumOfFinYr(inpDt: dt.datetime) -> int:
    """
    finStartMonday = first Monday before 1st Apr of this year
    inpMonday = first Monday before inpDt
    Week number will be the 1 + (inpMonday-finStartMonday)/7

    Args:
        inpDt (dt.datetime): input date

    Returns:
        int: week number as per financial year
    """

    # get first Monday before 1st Apr of this year
    finStartMonday = getMondayBeforeDt(dt.datetime(inpDt.year, 4, 1))

    # get first Monday before inpDt
    inpMonday = getMondayBeforeDt(inpDt)

    # get week number
    weekNum = 1 + ((inpMonday-finStartMonday).days/7)
    return int(weekNum)


def getFinYearForDt(inpDt: dt.datetime) -> int:
    """
    inpMonday = first monday before inpDt
    inpSun = inpMonday+6
    if inpSun.month >= april, then year is same as inpSun
    else year is one less than that of inpSun

    Args:
        inpDt (dt.datetime): input datetime

    Returns:
        int: financial year
    """
    # get first Monday before inpDt
    inpMonday = getMondayBeforeDt(inpDt)

    # inpSun = inpMonday+6
    inpSun = inpMonday+dt.timedelta(days=6)

    finYr = inpSun.year
    if inpSun.month < 4:
        finYr = inpSun.year - 1
    return finYr


def getMondayBeforeDt(inpDt: dt.datetime) -> dt.datetime:
    """ gets the first Monday before a specified date

    Args:
        inpDt (dt.datetime): input date

    Returns:
        dt.datetime: first monday before input date
    """
    # get first Monday before inpDt
    inpMonday = inpDt
    while not dt.datetime.strftime(inpMonday, '%w') == '1':
        inpMonday = inpMonday - dt.timedelta(days=1)
    return inpMonday


def getSundayAfterDt(inpDt: dt.datetime) -> dt.datetime:
    """ gets the first Sunday after a specified date

    Args:
        inpDt (dt.datetime): input date

    Returns:
        dt.datetime: first Sunday after input date
    """
    inpSunday = inpDt
    while not dt.datetime.strftime(inpSunday, '%w') == '0':
        inpSunday = inpSunday + dt.timedelta(days=1)
    return inpSunday
