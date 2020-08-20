import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.angleViolSummary import IAngleViolSummary


class AnglViolationsFetcher():
    """This class fetches Wide angle and adjescent angle violations summary for weekly report
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """

        self.connString = con_string

    def fetchAnglViolations(self, startDate: dt.datetime, endDate: dt.datetime) -> IAngleViolSummary:
        """fetch wide and adjescent angle violations summary 
        from derived db in the format of IAngleViolSummary
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            IAngleViolSummary: wide and adjescent angle violations summary for station pairs of the given time window
        """

        try:
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()

            sql_fetch = """ SELECT * FROM mis_warehouse.DAILY_ANGLE_DATA 
                        where (date_time BETWEEN TO_DATE(:col1, 'YYYY-MM-DD') and TO_DATE(:col2, 'YYYY-MM-DD'))
                        and not(entity='nan') 
                        order by date_time
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            df = pd.read_sql(sql_fetch, params={
                             'col1': startDate, 'col2': endDate}, con=connection)

        except:
            print('Error while fetching data from db')
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after iegc violation messages fetching')

        violMsgList: List[IIegcViolMsg] = []
        for i in df.index:
            violMsg: IIegcViolMsg = {
                'msgId': df['MESSAGE'][i],
                'date': dt.datetime.strftime(df['DATE_TIME'][i], "%d-%m-%Y"),
                'entity': df['ENTITY'][i],
                'schedule': df['SCHEDULE'][i],
                'drawal': df['DRAWAL'][i],
                'deviation': df['DEVIATION'][i]
            }
            violMsgList.append(violMsg)
        return violMsgList
