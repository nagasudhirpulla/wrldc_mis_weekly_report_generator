import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
from logging import Logger
import pandas as pd

appLogger: Logger = logging.getLogger()


class AppLogger:
    __instance: Logger = logging.getLogger()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AppLogger.__instance == None:
            raise Exception("app logger is not yet initialized")
        return AppLogger.__instance

    @staticmethod
    def initLogger(appConfig: dict):
        # formatting for log stash
        logstashFormatter = LogstashFormatter(
            message_type='python-logstash',
            extra=dict(application='mis_weekly_report_gen_service'))

        # set app logger name and minimum logging level
        appLogger = logging.getLogger('python-logstash-logger')
        appLogger.setLevel(logging.INFO)

        # configure console logging
        streamHandler = logging.StreamHandler()
        # streamHandler.setFormatter(logstashFormatter)
        appLogger.addHandler(streamHandler)

        # configure logstash logging
        host = appConfig["logstashHost"]
        port = appConfig["logstashPort"]
        if not(pd.isna(host)) and not(pd.isna(port)):
            logstashHandler = AsynchronousLogstashHandler(
                host, port, database_path='logstash.db')
            logstashHandler.setFormatter(logstashFormatter)
            appLogger.addHandler(logstashHandler)
        AppLogger.__instance = appLogger


def initAppLogger(appConfig: dict) -> Logger:
    AppLogger.initLogger(appConfig)
    return AppLogger.getInstance()


def getAppLogger() -> Logger:
    return AppLogger.getInstance()
