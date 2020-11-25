import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.lvNodesInfo import ILvNodesInfo
from src.appLogger import getAppLogger

class LvNodesInfoFetcher():
    """This class fetches LV Nodes info for weekly report
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """
        self.connString = con_string
        self.appLogger = getAppLogger()

    def fetchLvNodesInfo(self, startDate: dt.datetime, endDate: dt.datetime) -> List[ILvNodesInfo]:
        """fetch LV Nodes info for weekly report from warehouse db 
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            List[ILvNodesInfo]: List of LV Nodes info for weekly report
        """
        startDateLogString = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDateLogString = dt.datetime.strftime(endDate, '%Y-%m-%d')
        logExtra = {"startDate": startDateLogString,
                    "endDate": endDateLogString}
        try:
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()

            sql_fetch = """
                        select * from nodes_low_voltage_data \
                        where start_date IN 
                        (select max(start_date) as s from nodes_low_voltage_data)
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            df = pd.read_sql(sql_fetch, con=connection)
        except Exception as err:
            # print('Error while fetching data from db')
            self.appLogger.error(
                'error while LV Nodes data sql db fetch', exc_info=err, extra=logExtra)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after LV Nodes info fetching')

        lvNodesInfoList: List[ILvNodesInfo] = []
        for i in df.index:
            lvNodesInfoItem: ILvNodesInfo = {
                'nodes': df['NODES'][i],
                'season': df['SEASON_ANTECEDENT'][i],
                'description': df['DESCRIPTION_CONSTRAINTS'][i]
            }
            lvNodesInfoList.append(lvNodesInfoItem)
        return lvNodesInfoList
