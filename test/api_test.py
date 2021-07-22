from unittest import TestCase, mock
from utils.api import Api

class ApiTest(TestCase):
    def test_parse_parameter(self):
        api = Api()

        self.assertEqual(api.parse_parameters({"random":"param"}), "random=param")
        self.assertEqual(api.parse_parameters({"random":"param","random2":"param2"}), "random=param&random2=param2")
    

    def test_parse_paramenter_fail(self):
        api = Api()

        self.assertRaises(TypeError, api.parse_parameters, "fail")
        self.assertRaises(TypeError, api.parse_parameters, 123)
        self.assertRaises(TypeError, api.parse_parameters, ["fail"])
    

    def test_check_url(self):
        api = Api()

        self.assertEqual(api.check_url("https://google.com"), "https://google.com")
    

    def test_check_url_fail(self):
        api = Api()

        self.assertRaises(TypeError, api.check_url, {"failing": "test"})
        self.assertRaises(TypeError, api.check_url, ["failing", "test"])
        self.assertRaises(TypeError, api.check_url, 123)
        self.assertRaises(ValueError, api.check_url, "not a link")


    def test_build(self):
        api = Api()

        self.assertEqual(api.build(link="https://google.com"), "https://google.com")
        self.assertEqual(api.build(link="https://google.com", parameters={"random":"param"}), "https://google.com?random=param")
    

    def test_build_fail(self):
        api = Api()

        self.assertRaises(TypeError, api.build, link=["htt://google.com"])
        self.assertRaises(ValueError, api.build, link="htt://google.com")
        self.assertRaises(TypeError, api.build, link="http://google.com", parameters="asd")
        self.assertRaises(TypeError, api.build, link="http://google.com", parameters=["asd"])
        self.assertRaises(TypeError, api.build, link="http://google.com", parameters=123)


    def test_get(self):
        with mock.patch("utils.api.requests.get", return_value='called'):
            api = Api()

            self.assertIn("called", api.get(link="https://google.com"))


    def test_get_fail(self):
        with mock.patch("utils.api.requests.get", return_value='called'):
            api = Api()
            
            self.assertRaises(TypeError, api.get, link=["not a link"])
            self.assertRaises(ValueError, api.get, link= "Not a link")
            self.assertRaises(TypeError, api.get, link="http://google.com", parameters=123)