import sqlalchemy

class Database:
    def __init__(self, username="root", password="", host="localhost", port=3306, database=None):
        if database is None:
            raise ValueError("Key database is required")
        if type(database) is not str:
            raise TypeError("The key database must be a string")
        if type(username) is not str:
            raise TypeError("The key username must be a string")
        if type(password) is not str:
            raise TypeError("The key password must be a string")
        if type(host) is not str:
            raise TypeError("The key host must be a string")
        if type(port) is not int:
            raise TypeError("The key port must be an integer")
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