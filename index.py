import argparse
import datetime as dt
from src.utils.timeUtils import getMondayBeforeDt
from src.config.appConfig import getConfig
from src.typeDefs.appConfig import IAppConfig
from src.app.weeklyReportGenerator import WeeklyReportGenerator

# get start and end dates from command line
# initialise default command line input values
startDate = dt.datetime.now() - dt.timedelta(days=7)
startDate = getMondayBeforeDt(startDate)
endDate = startDate + dt.timedelta(days=6)

# get an instance of argument parser from argparse module
parser = argparse.ArgumentParser()
# setup arguements
parser.add_argument('--start_date', help="Enter Start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter last date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(endDate, '%Y-%m-%d'))
# get the dictionary of command line inputs entered by the user
args = parser.parse_args()

# access each command line input from the dictionary
startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.datetime.strptime(args.end_date, '%Y-%m-%d')

# get app db connection string from config file
appConfig: IAppConfig = getConfig()
appDbConStr: str = appConfig['appDbConStr']
dumpFolder: str = appConfig['dumpFolder']

# generate report word file
tmplPath = "assets/weekly_report_template.docx"

wklyRprtGntr = WeeklyReportGenerator(appDbConStr)
isSuccess: bool = wklyRprtGntr.generateWeeklyReport(
    startDate, endDate, tmplPath, dumpFolder)
if isSuccess:
    print('Weekly report word file generation done!')
else:
    print('Weekly report word file generation unsuccessful...')
