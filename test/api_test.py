import unittest
from utils.api import Api

class ApiTest(unittest.TestCase):
    def test_parse_parameter(self):
        api = Api()
        self.assertEqual(api.parse_parameters({"random":"param"}), ["random=param"])

    def test_build(self):
        api = Api()
        self.assertEqual(api.build(uri="https://google.com", parameters={"random":"param"}), "https://google.com?random=param")