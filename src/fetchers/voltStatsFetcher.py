import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, TypedDict
from src.appLogger import getAppLogger


class VoltStatsFetcher():
    """repo class to fetch derived voltage from mis_warehouse db.
    """

    def __init__(self, con_string):
        """constructor method
        Args:
            con_string ([type]): connection string
        """
        self.connString = con_string
        self.voltTable1 = []
        self.voltTable2 = []
        self.voltTable3 = []
        self.voltTable4 = []
        self.derivedVoltageDict = {'table1': self.voltTable1, 'table2': self.voltTable2,
                                   'table3': self.voltTable3, 'table4': self.voltTable4}
        self.appLogger = getAppLogger()

    def appendTables(self, df: pd.core.frame.DataFrame) -> None:
        """ append rows for each table for each day
        voltTable1 =[]
        voltTable2 =[]
        voltTable3 =[]
        voltTable4 =[]
        Args:
            df (pd.core.frame.DataFrame): pandas dataframe that contains derived voltage data for each day for all nodes.
        """
        date = df['DATE_KEY'][0].day

        dfTable1 = df.iloc[0:9]

        dfTable2 = df.iloc[9:18]
        dfTable2.reset_index(drop=True, inplace=True)

        dfTable3 = df.iloc[18:27]
        dfTable3.reset_index(drop=True, inplace=True)

        dfTable4 = df.iloc[27:]
        dfTable4.reset_index(drop=True, inplace=True)

        tempDictTable1 = {'date': date, 'amreliMax': dfTable1['MAXIMUM'][0], 'amreliMin': dfTable1['MINIMUM'][0], 'asojMax': dfTable1['MAXIMUM'][1], 'asojMin': dfTable1['MINIMUM'][1], 'bhilaiMax': dfTable1['MAXIMUM'][2], 'bhilaiMin': dfTable1['MINIMUM'][2], 'bhopalMax': dfTable1['MAXIMUM'][3], 'bhopalMin': dfTable1['MINIMUM'][3], 'boisarMax': dfTable1[
            'MAXIMUM'][4], 'boisarMin': dfTable1['MINIMUM'][4], 'damohMax': dfTable1['MAXIMUM'][5], 'damohMin': dfTable1['MINIMUM'][5], 'dehgamMax': dfTable1['MAXIMUM'][6], 'dehgamMin': dfTable1['MINIMUM'][6], 'dhuleMax': dfTable1['MAXIMUM'][7], 'dhuleMin': dfTable1['MINIMUM'][7], 'gwaliorMax': dfTable1['MAXIMUM'][8], 'gwaliorMin': dfTable1['MINIMUM'][8]}
        self.voltTable1.append(tempDictTable1)

        tempDictTable2 = {'date': date, 'indoreMax': dfTable2['MAXIMUM'][0], 'indoreMin': dfTable2['MINIMUM'][0], 'itarsiMax': dfTable2['MAXIMUM'][1], 'itarsiMin': dfTable2['MINIMUM'][1], 'jetpurMax': dfTable2['MAXIMUM'][2], 'jetpurMin': dfTable2['MINIMUM'][2], 'kalwaMax': dfTable2['MAXIMUM'][3], 'kalwaMin': dfTable2['MINIMUM'][3], 'karadMax': dfTable2[
            'MAXIMUM'][4], 'karadMin': dfTable2['MINIMUM'][4], 'kasorMax': dfTable2['MAXIMUM'][5], 'kasorMin': dfTable2['MINIMUM'][5], 'khandwaMax': dfTable2['MAXIMUM'][6], 'khandwaMin': dfTable2['MINIMUM'][6], 'nagdaMax': dfTable2['MAXIMUM'][7], 'nagdaMin': dfTable2['MINIMUM'][7], 'parliMax': dfTable2['MAXIMUM'][8], 'parliMin': dfTable2['MINIMUM'][8]}
        self.voltTable2.append(tempDictTable2)

        tempDictTable3 = {'date': date, 'raigarhMax': dfTable3['MAXIMUM'][0], 'raigarhMin': dfTable3['MINIMUM'][0], 'raipurMax': dfTable3['MAXIMUM'][1], 'raipurMin': dfTable3['MINIMUM'][1], 'vapiMax': dfTable3['MAXIMUM'][2], 'vapiMin': dfTable3['MINIMUM'][2], 'wardhaMax': dfTable3['MAXIMUM'][3], 'wardhaMin': dfTable3['MINIMUM'][3], 'binaMax': dfTable3[
            'MAXIMUM'][4], 'binaMin': dfTable3['MINIMUM'][4], 'durgMax': dfTable3['MAXIMUM'][5], 'durgMin': dfTable3['MINIMUM'][5], 'gwaliorMax': dfTable3['MAXIMUM'][6], 'gwaliorMin': dfTable3['MINIMUM'][6], 'indoreMax': dfTable3['MAXIMUM'][7], 'indoreMin': dfTable3['MINIMUM'][7], 'kotraMax': dfTable3['MAXIMUM'][8], 'kotraMin': dfTable3['MINIMUM'][8]}
        self.voltTable3.append(tempDictTable3)

        tempDictTable4 = {'date': date, 'sasanMax': dfTable4['MAXIMUM'][0], 'sasanMin': dfTable4['MINIMUM'][0], 'satnaMax': dfTable4['MAXIMUM'][1], 'satnaMin': dfTable4['MINIMUM'][1], 'seoniMax': dfTable4['MAXIMUM'][2], 'seoniMin': dfTable4['MINIMUM'][2], 'sipatMax': dfTable4['MAXIMUM']
                          [3], 'sipatMin': dfTable4['MINIMUM'][3], 'tamnarMax': dfTable4['MAXIMUM'][4], 'tamnarMin': dfTable4['MINIMUM'][4], 'vadodaraMax': dfTable4['MAXIMUM'][5], 'vadodaraMin': dfTable4['MINIMUM'][5], 'wardhaMax': dfTable4['MAXIMUM'][6], 'wardhaMin': dfTable4['MINIMUM'][6]}
        self.voltTable4.append(tempDictTable4)

    def fetchDerivedVoltage(self, startDate: dt.datetime, endDate: dt.datetime):
        """fetch derived voltage from mis_warehouse db 
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            derivedVoltageDict ={'table1':voltTable1,    
                                 'table2':voltTable2,
                                 'table3':voltTable3,
                                 'table4':voltTable4
                                 }
        """
        startDateLogString = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDateLogString = dt.datetime.strftime(endDate, '%Y-%m-%d')
        logExtra = {"startDate": startDateLogString,
                    "endDate": endDateLogString}
        # generating dates between startDate and endDate
        dates = []
        delta = endDate - startDate
        for i in range(delta.days + 1):
            dates.append(startDate + dt.timedelta(days=i))
        try:
            connection = cx_Oracle.connect(self.connString)
        except Exception as err:
            # print('error while creating a connection', err)
            self.appLogger.error(
                'error creating db connection for stationwise voltage stats', exc_info=err, extra=logExtra)
        else:
            print(connection.version)
            try:
                cur = connection.cursor()

                # fetching derived voltage data for each day.
                for date in dates:
                    fetch_sql = '''select  vt.date_key, vt.node_name,mt.node_voltage, vt.maximum, vt.minimum from 
                                derived_voltage vt, voltage_mapping_table mt
                                where  vt.mapping_id = mt.id and  mt.is_included_in_daily_voltage = 'T' and date_key = to_date(:start_date) '''

                    cur.execute(
                        "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD ' ")
                    df = pd.read_sql(fetch_sql, params={
                                     'start_date': date}, con=connection)

                    # sorting node_name alphabetically.
                    df.sort_values(['NODE_VOLTAGE', 'NODE_NAME'], ascending=[
                                   True, True], inplace=True, ignore_index=True)

                    # passing object to appendTables method.
                    df['MAXIMUM'] = df['MAXIMUM'].round().astype(int)
                    df['MINIMUM'] = df['MINIMUM'].round().astype(int)
                    self.appendTables(df)

            except Exception as err:
                # print('error while creating a cursor', err)
                self.appLogger.error(
                'error while stationwise voltage stats sql db fetch', exc_info=err, extra=logExtra)
            else:
                print('retrieval of derived voltage stats data complete')
                connection.commit()
        finally:
            cur.close()
            connection.close()
            print("connection closed")

        return self.derivedVoltageDict
