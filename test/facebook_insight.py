from unittest import TestCase
from dataframe.facebook_insight import FacebookInsight

json = [{
    "first": "text",
    "column": [
        {"action_type": "name", "value": 1.2}
    ]
}]

print("test")

class FacebookInsightTest(TestCase):
    def test_get_action(self):
        insight = FacebookInsight(json)
        self.assertEqual(insight.get_action("column", "name"), [1.2])

    def test_get_action_fail(self):
        insight = FacebookInsight(json)
        self.assertRaises(ValueError, insight.get_action)
        self.assertRaises(TypeError, insight.get_action, 123, "fail")
        self.assertRaises(TypeError, insight.get_action, "fail", 123)
    
    def test_sort(self):
        insight = FacebookInsight(json)
        self.assertEqual(insight.sort(column_name="first", ascending=True).to_dict(), insight.to_dict())
    
    def test_sort_fail(self):
        insight = FacebookInsight(json)
        self.assertRaises(ValueError, insight.sort)
        self.assertRaises(TypeError, insight.sort, column_name=123, ascending=True)
        self.assertRaises(TypeError, insight.sort, column_name="Test", ascending="Fail")