import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.ictConstraint import IIctConstraint
from src.appLogger import getAppLogger


class IctConstraintsFetcher():
    """This class fetches Ict Constraints for weekly report
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """
        self.connString = con_string
        self.appLogger = getAppLogger()

    def fetchIctConstraints(self, startDate: dt.datetime, endDate: dt.datetime) -> List[IIctConstraint]:
        """fetch Ict Constraints for weekly report from warehouse db 
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            List[IIctConstraint]: List of Ict Constraints for weekly report
        """
        startDateLogString = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDateLogString = dt.datetime.strftime(endDate, '%Y-%m-%d')
        logExtra = {"startDate": startDateLogString,
                    "endDate": endDateLogString}
        try:
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()
            sql_fetch = """
                        select * from ict_constraint_data 
                        where 
                        start_date IN (select max(start_date) as s from ict_constraint_data)
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            df = pd.read_sql(sql_fetch, con=connection)
        except Exception as err:
            # print('Error while fetching data from db')
            self.appLogger.error(
                'error while ict constraints sql db fetch', exc_info=err, extra=logExtra)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after ict constraints fetching')

        ictConstraints: List[IIctConstraint] = []
        for i in df.index:
            ictCons: IIctConstraint = {
                'ict': df['ICT'][i],
                'season': df['SEASON_ANTECEDENT'][i],
                'description': df['DESCRIPTION_CONSTRAINTS'][i]
            }
            ictConstraints.append(ictCons)
        return ictConstraints
