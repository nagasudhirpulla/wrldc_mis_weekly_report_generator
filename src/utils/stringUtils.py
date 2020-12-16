import re
from typing import List


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
    if outageTag == None:
        return outageTag, reason, remarks
    strippedOutageTag = outageTag.strip().lower()
    if strippedOutageTag == 'outage':
        outageTag = None
    else:
        if not(reason == None) and (strippedOutageTag == reason.strip().lower()):
            reason = None
        if not(remarks == None) and (strippedOutageTag == remarks.strip().lower()):
            remarks = None
    if strippedOutageTag in ["manually opened due to high voltage"]:
        undesiredRemarks = ["mohv"]
        undesiredStartRegexStr = r'^(mohv\.?|vr\.?)'
        reason = removeUndesiredRemarksAndStartWords(
            reason, undesiredRemarks, undesiredStartRegexStr)
        remarks = removeUndesiredRemarksAndStartWords(
            remarks, undesiredRemarks, undesiredStartRegexStr)
    elif strippedOutageTag in ["voltage regulation"]:
        undesiredRemarks = ["vr"]
        undesiredStartRegexStr = r'^vr\.?'
        reason = removeUndesiredRemarksAndStartWords(
            reason, undesiredRemarks, undesiredStartRegexStr)
        remarks = removeUndesiredRemarksAndStartWords(
            remarks, undesiredRemarks, undesiredStartRegexStr)
    elif strippedOutageTag in ["rsd"]:
        undesiredRemarks = ["rsd."]
        undesiredStartRegexStr = r'^rsd\.?'
        reason = removeUndesiredRemarksAndStartWords(
            reason, undesiredRemarks, undesiredStartRegexStr)
        remarks = removeUndesiredRemarksAndStartWords(
            remarks, undesiredRemarks, undesiredStartRegexStr)

    if (not(reason == None) and reason.strip() == ""):
        reason = None

    if (not(remarks == None) and remarks.strip() == ""):
        remarks = None

    return outageTag, reason, remarks


def combineTagReasonRemarks(tag, reas, rem):
    reasonStr = ' / '.join([r for r in [tag, reas,
                                        rem] if not(r == None) and not(r.strip() == "")])
    return reasonStr


def removeUndesiredRemarksAndStartWords(rStr, undesiredRemarks: List[str], undesiredStartRegexStr: str):
    if not(rStr == None):
        replaceRegex = re.compile(undesiredStartRegexStr, re.IGNORECASE)
        if (rStr.strip().lower() in undesiredRemarks):
            rStr = None
        else:
            # perform case insensitive replace in reason https://stackoverflow.com/a/14817425/2746323
            rStr = replaceRegex.sub('', rStr.strip())
    return rStr
