from unittest import TestCase, mock
from helper.facebook import Facebook

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
    