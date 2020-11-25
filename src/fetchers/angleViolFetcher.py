import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.angleViolSummary import IAngleViolSummary
from src.typeDefs.angleViolation import IAngleViolation
from src.appLogger import getAppLogger


class AnglViolationsFetcher():
    """This class fetches Wide angle and adjescent angle violations summary for weekly report
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """

        self.connString = con_string
        self.appLogger = getAppLogger()

    def fetchPairsAnglViolations(self, startDate: dt.datetime, endDate: dt.datetime) -> IAngleViolSummary:
        """fetch wide and adjescent angle violations summary 
        from derived db in the format of IAngleViolSummary
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            IAngleViolSummary: wide and adjescent angle violations summary for station pairs of the given time window
        """
        startDateLogString = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDateLogString = dt.datetime.strftime(endDate, '%Y-%m-%d')
        logExtra = {"startDate": startDateLogString,
                    "endDate": endDateLogString}
        try:
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()

            sql_fetch = """ 
                        SELECT angle_pair, MAX(angular_limit) as ang_lim,
                            AVG(viol_perc) as viol_perc, MAX(max_viol) as max_viol,
                            MIN(min_viol) as min_viol
                        FROM (
                                SELECT id, data_date, angle_pair,
                                    coalesce(angular_limit, 0) AS angular_limit,
                                    coalesce(viol_perc, 0) AS viol_perc,
                                    max_viol,
                                    min_viol,
                                    data_type
                                FROM mis_warehouse.daily_angles_data
                                WHERE 
                                data_type = :anglType and 
                                data_date between to_date(:start_date) and to_date(:end_date)
                            ) angl_data
                        GROUP BY angle_pair 
                        ORDER BY angle_pair
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            wideAnglDf = pd.read_sql(sql_fetch, params={
                'start_date': startDate, 'end_date': endDate, 'anglType': 'wide'}, con=connection)
            adjAnglDf = pd.read_sql(sql_fetch, params={
                'start_date': startDate, 'end_date': endDate, 'anglType': 'adj'}, con=connection)
        except Exception as err:
            # print('Error while fetching pair angle violation data from db')
            # print(e)
            self.appLogger.error(
                'error while executing angle pairs sepration data fetch sql', exc_info=err, extra=logExtra)
            res: IAngleViolSummary = {
                'wideAnglViols': [],
                'adjAnglViols': []
            }
            return res
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after pair angle violation data fetching')

        wideAnglViols: List[IAngleViolation] = []
        for i in wideAnglDf.index:
            pairViol: IAngleViolation = {
                'pairName': wideAnglDf['ANGLE_PAIR'][i],
                'angularLim': round(wideAnglDf['ANG_LIM'][i], 2),
                'violPerc': round(wideAnglDf['VIOL_PERC'][i], 2),
                'maxDeg': round(wideAnglDf['MAX_VIOL'][i], 2),
                'minDeg': round(wideAnglDf['MIN_VIOL'][i], 2),
            }
            wideAnglViols.append(pairViol)

        adjAngViols: List[IAngleViolation] = []
        for i in adjAnglDf.index:
            pairViol = {
                'pairName': adjAnglDf['ANGLE_PAIR'][i],
                'angularLim': round(adjAnglDf['ANG_LIM'][i], 2),
                'violPerc': round(adjAnglDf['VIOL_PERC'][i], 2),
                'maxDeg': round(adjAnglDf['MAX_VIOL'][i], 2),
                'minDeg': round(adjAnglDf['MIN_VIOL'][i], 2),
            }
            adjAngViols.append(pairViol)

        violSumm: IAngleViolSummary = {
            'wideAnglViols': wideAnglViols,
            'adjAnglViols': adjAngViols
        }

        return violSumm
