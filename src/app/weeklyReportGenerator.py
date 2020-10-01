import os
import datetime as dt
from src.utils.timeUtils import getWeekNumOfFinYr, getFinYearForDt, getMondayBeforeDt
from src.fetchers.genUnitOutagesFetcher import fetchMajorGenUnitOutages
from src.fetchers.transElOutagesFetcher import fetchTransElOutages
from src.fetchers.longTimeUnrevivedForcedOutagesFetcher import fetchlongTimeUnrevivedForcedOutages
from src.fetchers.freqProfileFetcher import FrequencyProfileFetcher
from src.fetchers.vdiFetcher import VdiFetcher
from src.fetchers.voltStatsFetcher import VoltStatsFetcher
from src.fetchers.angleViolFetcher import AnglViolationsFetcher
from src.fetchers.iegcViolMsgsFetcher import IegcViolMsgsFetcher
from src.fetchers.ictConstraintsFetcher import IctConstraintsFetcher
from src.fetchers.transmissionConstraintsFetcher import TransConstraintsFetcher
from src.fetchers.hvNodesInfoFetcher import HvNodesInfoFetcher
from src.fetchers.lvNodesInfoFetcher import LvNodesInfoFetcher
from src.typeDefs.stationwiseVdiData import IStationwiseVdi
from src.typeDefs.outage import IOutage
from src.typeDefs.iegcViolMsg import IIegcViolMsg
from src.typeDefs.angleViolSummary import IAngleViolSummary
from src.typeDefs.ictConstraint import IIctConstraint
from src.typeDefs.transConstraint import ITransConstraint
from src.typeDefs.hvNodesInfo import IHvNodesInfo
from src.typeDefs.lvNodesInfo import ILvNodesInfo
from src.typeDefs.appConfig import IAppConfig
from src.typeDefs.reportContext import IReportCxt
from typing import List
from docxtpl import DocxTemplate, InlineImage
# from docx2pdf import convert


class WeeklyReportGenerator:
    appDbConStr: str = ''

    def __init__(self, appDbConStr: str):
        self.appDbConStr = appDbConStr

    def getReportContextObj(self, startDate: dt.datetime, endDate: dt.datetime) -> IReportCxt:
        """get the report context object for populating the weekly report template

        Args:
            startDate (dt.datetime): start date object
            endDate (dt.datetime): end date object

        Returns:
            IReportCxt: report context object
        """
        endDate = endDate.replace(hour=23, minute=59, second=59)
        startDateReportString = dt.datetime.strftime(startDate, '%d-%b-%Y')
        endDateReportString = dt.datetime.strftime(endDate, '%d-%b-%Y')
        weekNum = getWeekNumOfFinYr(startDate)
        finYr = getFinYearForDt(startDate)
        finYrStr = '{0}-{1}'.format(finYr, (finYr+1) % 100)

        # create context for weekly reoport
        # initialise report context
        reportContext: IReportCxt = {
            'startDtObj': startDate,
            'endDtObj': endDate,
            'startDt': startDateReportString,
            'endDt': endDateReportString,
            'wkNum': weekNum,
            'finYr': finYrStr,
            'genOtgs': [],
            'transOtgs': [],
            'longTimeOtgs': [],
            'freqProfRows': [],
            'weeklyFdi': -1,
            'wideViols': [],
            'adjViols': [],
            'voltStats': {
                'table1': [],
                'table2': [],
                'table3': [],
                'table4': []
            },
            'ictCons': [],
            'transCons': [],
            'lvNodes': [],
            'hvNodes': []
        }

        # get major generating unit outages
        reportContext['genOtgs'] = fetchMajorGenUnitOutages(
            self.appDbConStr, startDate, endDate)

        # get transmission element outages
        reportContext['transOtgs'] = fetchTransElOutages(
            self.appDbConStr, startDate, endDate)

        # get long time unrevived transmission element outages
        reportContext['longTimeOtgs'] = fetchlongTimeUnrevivedForcedOutages(
            self.appDbConStr, startDate, endDate)

        # get freq profile data
        freqProfFetcher = FrequencyProfileFetcher(self.appDbConStr)
        freqProfile = freqProfFetcher.fetchDerivedFrequency(startDate, endDate)
        reportContext['freqProfRows'] = freqProfile['freqProfRows']
        reportContext['weeklyFdi'] = "{:0.2f}".format(freqProfile['weeklyFdi'])

        # get stationwise vdi data
        vdiFetcher = VdiFetcher(self.appDbConStr)
        vdiData: IStationwiseVdi = vdiFetcher.fetchWeeklyVDI(startDate)
        reportContext['vdi400Rows'] = vdiData['vdi400Rows']
        reportContext['vdi765Rows'] = vdiData['vdi765Rows']

        # get stationwise voltage stats
        voltStatsFetcher = VoltStatsFetcher(self.appDbConStr)
        voltStats: dict = voltStatsFetcher.fetchDerivedVoltage(
            startDate, endDate)
        reportContext['voltStats'] = voltStats

        # get iegc violation messages
        violMsgsFetcher = IegcViolMsgsFetcher(self.appDbConStr)
        violMsgs: List[IIegcViolMsg] = violMsgsFetcher.fetchIegcViolMsgs(
            startDate, endDate)
        reportContext['violMsgs'] = violMsgs

        # get pairs angle violations
        anglViolsFetcher = AnglViolationsFetcher(self.appDbConStr)
        pairAnglViolations: IAngleViolSummary = anglViolsFetcher.fetchPairsAnglViolations(
            startDate, endDate)
        reportContext['wideViols'] = pairAnglViolations['wideAnglViols']
        reportContext['adjViols'] = pairAnglViolations['adjAnglViols']

        # get ict constraints
        ictConsFetcher = IctConstraintsFetcher(self.appDbConStr)
        ictConsList: List[IIctConstraint] = ictConsFetcher.fetchIctConstraints(
            startDate, endDate)
        reportContext['ictCons'] = ictConsList

        # get transmission constraints
        transConsFetcher = TransConstraintsFetcher(self.appDbConStr)
        transConsList: List[ITransConstraint] = transConsFetcher.fetchTransConstraints(
            startDate, endDate)
        reportContext['transCons'] = transConsList

        # get HV Nodes Info
        hvNodesFetcher = HvNodesInfoFetcher(self.appDbConStr)
        hvNodesInfoList: List[IHvNodesInfo] = hvNodesFetcher.fetchHvNodesInfo(
            startDate, endDate)
        reportContext['hvNodes'] = hvNodesInfoList

        # get LV Nodes Info
        lvNodesFetcher = LvNodesInfoFetcher(self.appDbConStr)
        lvNodesInfoList: List[ILvNodesInfo] = lvNodesFetcher.fetchLvNodesInfo(
            startDate, endDate)
        reportContext['lvNodes'] = lvNodesInfoList

        return reportContext

    def generateReportWithContext(self, reportContext: IReportCxt, tmplPath: str, dumpFolder: str) -> bool:
        """generate the report file at the desired dump folder location 
        based on the template file and report context object

        Args:
            reportContext (IReportCxt): report context object
            tmplPath (str): full file path of the template
            dumpFolder (str): folder path for dumping the generated report

        Returns:
            bool: True if process is success, else False
        """
        doc = DocxTemplate(tmplPath)

        # # signature Image
        # signatureImgPath = 'assets/signature.png'
        # signImg = InlineImage(doc, signatureImgPath)
        # reportContext['signature'] = signImg

        doc.render(reportContext)
        dumpFileName = 'Weekly_no_{0}_{1}_to_{2}.docx'.format(reportContext['wkNum'], dt.datetime.strftime(
            reportContext['startDtObj'], '%d-%m-%Y'), dt.datetime.strftime(reportContext['endDtObj'], '%d-%m-%Y'))
        dumpFileFullPath = os.path.join(dumpFolder, dumpFileName)
        doc.save(dumpFileFullPath)
        return True

    def generateWeeklyReport(self, startDt: dt.datetime, endDt: dt.datetime, tmplPath: str, dumpFolder: str) -> bool:
        """generates and dumps weekly report for given dates at a desired location based on a template file

        Args:
            startDt (dt.datetime): start date
            endDt (dt.datetime): end date
            tmplPath (str): full file path of the template file
            dumpFolder (str): folder path where the generated reports are to be dumped

        Returns:
            bool: True if process is success, else False
        """
        reportCtxt = self.getReportContextObj(startDt, endDt)
        isSuccess = self.generateReportWithContext(
            reportCtxt, tmplPath, dumpFolder)
        # convert report to pdf
        # convert(dumpFileFullPath, dumpFileFullPath.replace('.docx', '.pdf'))
        return isSuccess
