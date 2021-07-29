import sqlalchemy

class Database:
    def __init__(self, username="root", password="", host="localhost", port="3306", database=None):
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._database = database
    
    def initialize(self):
        return sqlalchemy.create_engine(
            "mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            .format(username=self._username, password=self._password, host=self._host, port=self._port, database=self._database)
            )