from typing import Optional


def addTrailingZeroForTimeComp(nVal: int) -> str:
    """add trailing zero to number <10

    Args:
        nVal (int): input number

    Returns:
        str: output string
    """
    if nVal < 10 and nVal >= 0:
        return '0{0}'.format(nVal)
    else:
        return '{0}'.format(nVal)


def convertHrsToSpanStr(nHrs) -> str:
    """convert number of hours to string, like 29.6 to 29:36

    Args:
        nHrs ([type]): [description]

    Returns:
        str: [description]
    """
    hrs = addTrailingZeroForTimeComp(int(nHrs // 1))
    mins = addTrailingZeroForTimeComp(int(round((nHrs % 1)*60)))
    spanStr = '{0}:{1}'.format(hrs, mins)
    return spanStr


def removeRedundantRemarks(outageTag, reason, remarks):
    """Removes redundant reason or remarks if they are matching with outage tag

    Args:
        outageTag ([type]): outageTag
        reason ([type]): reason
        remarks ([type]): remarks

    Returns:
        outageTag, reason, remarks: corrected outageTag, reason and remarks
    """    
    if outageTag == 'Outage':
        outageTag = None
    else:
        strippedOutageTag = outageTag.strip().lower()
        if not(reason == None) and (strippedOutageTag == reason.strip().lower()):
            reason = None
        if not(remarks == None) and (strippedOutageTag == remarks.strip().lower()):
            remarks = None
    return outageTag, reason, remarks
