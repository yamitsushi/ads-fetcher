from unittest import TestCase, mock
from helper.facebook import Facebook

def mocked_get_requests(*args):
    class MockResponse:
        def __init__(self, json_data, status):
            self.text = json_data
            self.status_code = status
        def json(self):
            return self.text
    if args[1]["access_token"] == "valid":
        return MockResponse({
            "validity": True
        }, 200)
    if args[1]["access_token"] == "invalid":
        return MockResponse({
            "validity": False
        }, 400)
    return MockResponse({
    }, 500)


class FacebookTest(TestCase):
    """Facebook Builder"""
    def test_facebook_fail(self):
        self.assertRaises(TypeError, Facebook, graph_url=["invalid"])
        self.assertRaises(TypeError, Facebook, graph_url=123)
        self.assertRaises(TypeError, Facebook, graph_version=123)
        self.assertRaises(TypeError, Facebook, api="asdf")

    """Token Tester"""
    def test_token_string(self):
        facebook = Facebook()
        self.assertRaises(TypeError, facebook.set_token, token=123)

    def test_token_blank(self):
        facebook = Facebook()
        self.assertRaises(ValueError, facebook.set_token, token="")
    
    """Account Tester"""
    def test_account_string(self):
        facebook = Facebook()
        self.assertRaises(TypeError, facebook.set_account, account=123)

    def test_account_blank(self):
        facebook = Facebook()
        self.assertRaises(ValueError, facebook.set_account, account="")

    """Fields Tester"""
    def test_field_string(self):
        facebook = Facebook()
        self.assertRaises(TypeError, facebook.set_field, field=123)

    def test_field_blank(self):
        facebook = Facebook()
        self.assertRaises(ValueError, facebook.set_field, field="")
    
    """Level Tester"""
    def test_level_string(self):
        facebook = Facebook()
        self.assertRaises(TypeError, facebook.set_level, level=123)

    def test_level_blank(self):
        facebook = Facebook()
        self.assertRaises(ValueError, facebook.set_level, level="")

    """Time Range Tester"""
    def test_range_object(self):
        facebook = Facebook()
        self.assertRaises(TypeError, facebook.set_range, range="Invalid")
        self.assertRaises(ValueError, facebook.set_range, range={})
        self.assertRaises(TypeError, facebook.set_range, range={"since": 123, "until": ""})
        self.assertRaises(TypeError, facebook.set_range, range={"since": "", "until": 123})

    """Token Tester"""
    def test_token_validity(self):
        with mock.patch("utils.api.requests.get", side_effect=mocked_get_requests):
            facebook = Facebook()
            facebook.set_token("valid")
            self.assertEqual(facebook.test_token_insight(), True)
    
    def test_token_validity_fail(self):
        with mock.patch("utils.api.requests.get", side_effect=mocked_get_requests):
            facebook = Facebook()
            self.assertRaises(ValueError, facebook.test_token_insight)
            facebook.set_token("invalid")
            self.assertEqual(facebook.test_token_insight(), False)