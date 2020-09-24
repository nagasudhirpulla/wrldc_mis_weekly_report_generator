import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.dayFreqProfile import IDayFreqProfile
from src.typeDefs.freqProfileData import IFreqProfile


class FrequencyProfileFetcher():
    """This class fetches derived frequency for frequency profile section in weekly report
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """

        self.connString = con_string

    def toContextDict(self, df: pd.core.frame.DataFrame) -> IFreqProfile:
        """ return derivedFrequencyDict that has two keys 'freqProfRows', 'weeklyFDI'
        Args:
            df (pd.core.frame.DataFrame):pandas dataframe
        Returns:
            IFreqProfile: frequency profile data
        """

        # initialise frequency profile data
        derFrequencyDict: IFreqProfile = {
            'freqProfRows': [],
            'weeklyFdi': -1
        }

        if df.shape[0] == 0:
            return derFrequencyDict

        del df['ID']
        df['DATE_KEY'] = df['DATE_KEY'].dt.day

        derFreqRows = []
        weeklyFDI = (df['OUT_OF_BAND_INHRS'].sum())/168
        for ind in df.index:
            tempDict = {
                'date_day': df['DATE_KEY'][ind],
                'max_freq': "{:0.2f}".format(df['MAXIMUM'][ind]),
                'min_freq': "{:0.2f}".format(df['MINIMUM'][ind]),
                'avg_freq': "{:0.2f}".format(df['AVERAGE'][ind]),
                'less_than_band': "{:0.2f}".format(df['LESS_THAN_BAND'][ind]),
                'bw_band': "{:0.2f}".format(df['BETWEEN_BAND'][ind]),
                'great_than_band': "{:0.2f}".format(df['GREATER_THAN_BAND'][ind]),
                'out_of_band': "{:0.2f}".format(df['OUT_OF_BAND'][ind]),
                'out_hrs': "{:0.2f}".format(df['OUT_OF_BAND_INHRS'][ind]),
                'fdi': "{:0.2f}".format(df['FDI'][ind])
            }
            derFreqRows.append(tempDict)
        derFrequencyDict['freqProfRows'] = derFreqRows
        derFrequencyDict['weeklyFdi'] = weeklyFDI

        return derFrequencyDict

    def fetchDerivedFrequency(self, startDate: dt.datetime, endDate: dt.datetime) -> IFreqProfile:
        """fetch derived frequency from mis_warehouse db 
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            IFreqProfile: frequency profile data
        """

        try:
            connection = cx_Oracle.connect(self.connString)
        except Exception as err:
            print('error while creating a connection', err)

        else:
            # print(connection.version)
            try:
                cur = connection.cursor()
                fetch_sql = '''select *
                            from mis_warehouse.derived_frequency
                            where date_key between to_date(:start_date) and to_date(:end_date) 
                            order by date_key'''

                cur.execute(
                    "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD ' ")
                df = pd.read_sql(fetch_sql, params={
                                 'start_date': startDate, 'end_date': endDate}, con=connection)

            except Exception as err:
                print('error while fetching derived freq data for weekly report', err)
            else:
                print('derived freq data fetch complete')
                connection.commit()
        finally:
            cur.close()
            connection.close()
            print("db connection closed after freq profile data fetch for weekly report")
        derivedFrequencyDict = self.toContextDict(df)
        return derivedFrequencyDict
