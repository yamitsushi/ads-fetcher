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
            "validity": True,
            "data": []
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

    """Token Tester"""
    def test_token_validity(self):
        with mock.patch("utils.api.requests.get", side_effect=mocked_get_requests):
            facebook = Facebook()
            facebook.set_token("valid")
            self.assertEqual(facebook.is_token_valid(), True)
    
    def test_token_validity_fail(self):
        with mock.patch("utils.api.requests.get", side_effect=mocked_get_requests):
            facebook = Facebook()
            self.assertRaises(ValueError, facebook.is_token_valid)
            facebook.set_token("invalid")
            self.assertEqual(facebook.is_token_valid(), False)

    def test_get_insight(self):
        with mock.patch("utils.api.requests.get", side_effect=mocked_get_requests):
            facebook = Facebook()
            facebook.set_account("act_number")
            facebook.set_field("sample_fields")
            facebook.set_level("sample_level")
            facebook.set_token("valid")
            response = facebook.get_insight(since="2021-07-04", until="2021-07-10")
            self.assertEqual(type(response.text["data"]), list)

    def test_get_insight_fail(self):
        with mock.patch("utils.api.requests.get", side_effect=mocked_get_requests):
            for key in range(5):
                facebook = Facebook()
                if key == 0 or key != 1:
                    facebook.set_account("act_number")
                if key == 0 or key != 2:
                    facebook.set_level("sample_level")
                if key == 0 or key != 3:
                    facebook.set_token("sample_token")
                if key == 0 or key != 4:
                    facebook.set_field("sample_fields")
                self.assertRaises(ValueError,facebook.get_insight)

            facebook = Facebook()
            facebook.set_account("act_number")
            facebook.set_level("sample_level")
            facebook.set_token("sample_token")
            facebook.set_field("sample_fields")
            self.assertRaises(ValueError,facebook.get_insight, since="2021-07-04")
            self.assertRaises(ValueError,facebook.get_insight, until="2021-07-04")
            self.assertRaises(TypeError,facebook.get_insight, since="2021-07-04", until=123)
            self.assertRaises(TypeError,facebook.get_insight, since=123, until="2021-07-04")