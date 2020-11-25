from typing import TypedDict


class IAppConfig(TypedDict):
    appDbConStr: str
    dumpFolder: str
    flaskSecret: str
    flaskPort: str
    logstashHost: str
    logstashPort: int
