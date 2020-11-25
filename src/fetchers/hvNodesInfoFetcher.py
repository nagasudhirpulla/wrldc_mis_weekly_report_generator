import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.hvNodesInfo import IHvNodesInfo
from src.appLogger import getAppLogger


class HvNodesInfoFetcher():
    """This class fetches HV Nodes info for weekly report
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """
        self.connString = con_string
        self.appLogger = getAppLogger()

    def fetchHvNodesInfo(self, startDate: dt.datetime, endDate: dt.datetime) -> List[IHvNodesInfo]:
        """fetch HV Nodes info for weekly report from warehouse db 
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            List[IHvNodesInfo]: List of HV Nodes info for weekly report
        """
        startDateLogString = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDateLogString = dt.datetime.strftime(endDate, '%Y-%m-%d')
        logExtra = {"startDate": startDateLogString,
                    "endDate": endDateLogString}
        try:
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()

            sql_fetch = """
                        select * from nodes_high_voltage_data 
                        where start_date IN 
                        (select max(start_date) as s from nodes_high_voltage_data)
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            df = pd.read_sql(sql_fetch, con=connection)
        except Exception as err:
            # print('Error while fetching data from db')
            self.appLogger.error(
                'error while HV Nodes data sql db fetch', exc_info=err, extra=logExtra)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after HV Nodes info fetching')

        hvNodesInfoList: List[IHvNodesInfo] = []
        for i in df.index:
            hvNodesInfoItem: IHvNodesInfo = {
                'nodes': df['NODES'][i],
                'season': df['SEASON_ANTECEDENT'][i],
                'description': df['DESCRIPTION_CONSTRAINTS'][i]
            }
            hvNodesInfoList.append(hvNodesInfoItem)
        return hvNodesInfoList
