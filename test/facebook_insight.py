from unittest import TestCase
from dataframe.facebook_insight import FacebookInsight

json = [{
    "first": "text",
    "column": [
        {"action_type": "name", "value": 1.2}
    ]
}]

class FacebookInsightTest(TestCase):
    def test_get_action(self):
        insight = FacebookInsight(json)
        self.assertEqual(insight.get_action("column", "name"), [1.2])

    def test_get_action_fail(self):
        insight = FacebookInsight(json)
        self.assertRaises(ValueError, insight.get_action)
        self.assertRaises(TypeError, insight.get_action, 123, "fail")
        self.assertRaises(TypeError, insight.get_action, "fail", 123)