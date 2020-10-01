from typing import TypedDict, List
from src.typeDefs.outage import IOutage
from src.typeDefs.dayFreqProfile import IDayFreqProfile
from src.typeDefs.stationVdiProfile import IStationVdiProfile
from src.typeDefs.iegcViolMsg import IIegcViolMsg
from src.typeDefs.ictConstraint import IIctConstraint
from src.typeDefs.transConstraint import ITransConstraint
from src.typeDefs.lvNodesInfo import ILvNodesInfo
from src.typeDefs.hvNodesInfo import IHvNodesInfo
import datetime as dt

class VoltageStatsDict(TypedDict):
    table1: List[dict]
    table2: List[dict]
    table3: List[dict]
    table4: List[dict]


class IReportCxt(TypedDict):
    startDtObj: dt.datetime
    endDtObj: dt.datetime
    startDt: str
    endDt: str
    wkNum: float
    finYr: str
    genOtgs: List[IOutage]
    transOtgs: List[IOutage]
    longTimeOtgs: List[IOutage]
    freqProfRows: List[IDayFreqProfile]
    weeklyFdi: float
    vdi400Rows: List[IStationVdiProfile]
    vdi765Rows: List[IStationVdiProfile]
    violMsgs: List[IIegcViolMsg]
    voltStats: VoltageStatsDict
    ictCons: List[IIctConstraint]
    transCons: List[ITransConstraint]
    hvNodes: List[IHvNodesInfo]
    lvNodes: List[ILvNodesInfo]
