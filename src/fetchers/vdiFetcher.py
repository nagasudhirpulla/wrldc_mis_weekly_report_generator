import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.stationwiseVdiData import IStationwiseVdi
from src.typeDefs.stationVdiProfile import IStationVdiProfile
from src.utils.stringUtils import convertHrsToSpanStr
from src.appLogger import getAppLogger


class VdiFetcher():
    """fetches VDI data for populating weekly mis report
    """

    def __init__(self, appDbConnStr: str):
        """constructor method
        Args:
            con_string ([type]): connection string of application db that contains VDI derived data
        """

        self.connString = appDbConnStr
        self.appLogger = getAppLogger()

    def toDerivedVDIDict(self, df: pd.core.frame.DataFrame) -> IStationwiseVdi:
        """returns derivedVDIDict that has two keys 
        derivedVDIDict['VDIRows400'] = VDIRows400Kv
        derivedVDIDict['VDIRows765'] = VDIRows765Kv
        Args:
            df (pd.core.frame.DataFrame): pandas dataframe
        Returns:
            IStationwiseVdi: week VDI summary data for each 765 and 400 kv station 
        """

        del[df['ID'], df['MAPPING_ID'], df['WEEK_START_DATE']]
        VDIRows400Kv: List[IStationVdiProfile] = []
        VDIRows765Kv: List[IStationVdiProfile] = []
        derivedVDIDict: IStationwiseVdi = {
            'vdi400Rows': [],
            'vdi765Rows': []
        }

        group = df.groupby("NODE_VOLTAGE")
        for nameOfGroup, groupDf in group:
            if nameOfGroup == 400:
                for ind in groupDf.index:
                    tempDict = {
                        'station': groupDf['NODE_NAME'][ind],
                        'maxVol': groupDf['MAXIMUM'][ind],
                        'minVol': groupDf['MINIMUM'][ind],
                        'lessThanBand': "{:0.2f}".format(groupDf['LESS_THAN_BAND'][ind]),
                        'bwBand': "{:0.2f}".format(groupDf['BETWEEN_BAND'][ind]),
                        'greatThanBand': "{:0.2f}".format(groupDf['GREATER_THAN_BAND'][ind]),
                        'lessBandHrs': convertHrsToSpanStr(groupDf['LESS_THAN_BAND_INHRS'][ind]),
                        'greatBandHrs': convertHrsToSpanStr(groupDf['GREATER_THAN_BAND_INHRS'][ind]),
                        'outOfBandHrs': convertHrsToSpanStr(groupDf['OUT_OF_BAND_INHRS'][ind]),
                        'vdi': "{:0.2f}".format(groupDf['VDI'][ind])
                    }
                    VDIRows400Kv.append(tempDict)
            elif nameOfGroup == 765:
                for ind in groupDf.index:
                    tempDict = {
                        'station': groupDf['NODE_NAME'][ind],
                        'maxVol': groupDf['MAXIMUM'][ind],
                        'minVol': groupDf['MINIMUM'][ind],
                        'lessThanBand': "{:0.2f}".format(groupDf['LESS_THAN_BAND'][ind]),
                        'bwBand': "{:0.2f}".format(groupDf['BETWEEN_BAND'][ind]),
                        'greatThanBand': "{:0.2f}".format(groupDf['GREATER_THAN_BAND'][ind]),
                        'lessBandHrs': convertHrsToSpanStr(groupDf['LESS_THAN_BAND_INHRS'][ind]),
                        'greatBandHrs': convertHrsToSpanStr(groupDf['GREATER_THAN_BAND_INHRS'][ind]),
                        'outOfBandHrs': convertHrsToSpanStr(groupDf['OUT_OF_BAND_INHRS'][ind]),
                        'vdi': "{:0.2f}".format(groupDf['VDI'][ind])
                    }
                    VDIRows765Kv.append(tempDict)
        derivedVDIDict['vdi400Rows'] = VDIRows400Kv
        derivedVDIDict['vdi765Rows'] = VDIRows765Kv
        return derivedVDIDict

    def fetchWeeklyVDI(self, startDate: dt.datetime) -> IStationwiseVdi:
        """fetched derived VDI from mis_warehouse db
        Args:
            startDate (dt.datetime): start-date
        Returns:
            IStationwiseVdi: week VDI summary data for each 765 and 400 kv station 
        """
        startDateLogString = dt.datetime.strftime(startDate, '%Y-%m-%d')
        logExtra = {"startDate": startDateLogString}
        try:
            connection = cx_Oracle.connect(self.connString)
        except Exception as err:
            # print('error while creating a connection', err)
            self.appLogger.error(
                'error creating db connection for VDI creation', exc_info=err, extra=logExtra)
        else:
            # print(connection.version)
            try:
                cur = connection.cursor()
                fetch_sql = '''select vdi.* from 
                            mis_warehouse.derived_vdi vdi, mis_warehouse.voltage_mapping_table mt
                            where vdi.mapping_id = mt.id and mt.is_included_in_weekly_vdi = 'T' and week_start_date = to_date(:start_date)'''

                cur.execute(
                    "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
                df = pd.read_sql(fetch_sql, params={
                                 'start_date': startDate}, con=connection)

            except Exception as err:
                # print('error while fetching weekly VDI data', err)
                self.appLogger.error(
                    'error while VDI sql db fetch', exc_info=err, extra=logExtra)
                return {'vdi400Rows': [], 'vdi765Rows': []}
            else:
                print('VDI data fetch complete')
                connection.commit()
        finally:
            cur.close()
            connection.close()
            print("db connection closed after weekly vdi fetch")
        df['MAXIMUM'] = df['MAXIMUM'].round().astype(int)
        df['MINIMUM'] = df['MINIMUM'].round().astype(int)
        derivedVDIDict = self.toDerivedVDIDict(df)
        return derivedVDIDict
