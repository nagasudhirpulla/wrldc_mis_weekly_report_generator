'''
This is the web server that acts as a service that creates outages raw data
'''
import datetime as dt
from src.config.appConfig import getConfig
from src.appLogger import initAppLogger
from src.config.appConfig import IAppConfig
from src.utils.timeUtils import getMondayBeforeDt, getSundayAfterDt
from src.app.weeklyReportGenerator import WeeklyReportGenerator
from flask import Flask, request, jsonify

# get application config
appConfig: IAppConfig = getConfig()

# initialize logger
appLogger = initAppLogger(appConfig)

app = Flask(__name__)

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']


@app.route('/')
def hello():
    return "This is the web server that acts as a service that creates MIS weekly report"


@app.route('/weekly_report', methods=['POST'])
def create_weekly_report():
    # get start and end dates from post request body
    reqData = request.get_json()
    try:
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
    except Exception as ex:
        return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400
    # get app db connection string from config file
    appConfig: IAppConfig = getConfig()
    appDbConStr: str = appConfig['appDbConStr']
    dumpFolder: str = appConfig['dumpFolder']
    # generate report word file
    tmplPath: str = "assets/weekly_report_template.docx"
    # create weekly report
    wklyRprtGntr = WeeklyReportGenerator(appDbConStr)
    # use while loop to create multiple reports at once
    currDt: dt.datetime = startDate
    while currDt <= endDate:
        currStartDt = getMondayBeforeDt(currDt)
        currEndDt = getSundayAfterDt(currStartDt)
        isWeeklyReportGenerationSuccess: bool = wklyRprtGntr.generateWeeklyReport(
            currStartDt, currEndDt, tmplPath, dumpFolder)
        currDt = currEndDt + dt.timedelta(days=1)
    if isWeeklyReportGenerationSuccess:
        return jsonify({'message': 'weekly report generation successful!!!', 'startDate': startDate, 'endDate': endDate})
    else:
        return jsonify({'message': 'weekly report generation was not success'}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
