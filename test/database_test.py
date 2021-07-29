from unittest import TestCase, mock
from utils.database import Database

def mocked_create_engine(*args):
    return args[0]

class DatabaseTest(TestCase):
    def test_database_call(self):
        self.assertIsInstance(Database(database="working"), Database)


    def test_database_call_fail(self):
        self.assertRaises(ValueError, Database)
        self.assertRaises(TypeError, Database, database=123)
        self.assertRaises(TypeError, Database, database="failing", username=123)
        self.assertRaises(TypeError, Database, database="failing", password=123)
        self.assertRaises(TypeError, Database, database="failing", port="")
    

    def test_database_initialize(self):
        with mock.patch("sqlalchemy.create_engine", side_effect=mocked_create_engine):
            database = Database(username="username", password="password", host="host", port=123, database="database")
            self.assertEqual(database.initialize(), "mysql+pymysql://username:password@host:123/database")