import sys

# Albert's HOME ###################################################################
sys.path.insert(0, '/Users/jcatama/Desktop/Projects/advertize.net/time-optimizer/')
###################################################################################

from tests.config_test import *
from utilities.m_facebook_ads import MFacebookAdsInsights

fb = MFacebookAdsInsights()
id_attr = 'act_2563373910645150'
fields = 'spend,actions'
date_preset = 'today'
str_hash = '/insights'
expected_query = '{}{}/insights?fields={}&date_preset={}&access_token={}'.format(FB_API, id_attr, fields, date_preset, FB_TOKEN)

def test_build_query():
  print('>> test_build_query')
  query = fb.build_query({'id_attr': id_attr, 'fields': fields, 'date_preset': date_preset })
  assert query == expected_query, "Should be same query string"

def test_build_query_error_query_string():
  print('>> test_build_query_error_query_string')
  query = fb.build_query({'id_attr': id_attr, 'fields': fields+',impressions', 'date_preset': date_preset })
  assert query != expected_query, "Should not be same query string"

def test_build_query_error_empty_args():
  print('>> test_build_query_error_empty_args')
  query = fb.build_query()
  assert isinstance(query, dict), "Should return an error message"

def test_get_200():
  print('>> test_get_200')
  q = fb.get(fb.build_query({'id_attr': id_attr, 'fields': fields, 'date_preset': date_preset }))
  assert q.status_code == 200, "Should return 200"

def test_get_400():
  print('>> test_get_400')
  q = fb.get(fb.build_query({'id_attr': id_attr+'1', 'fields': fields, 'date_preset': date_preset }))
  assert q.status_code == 400, "Should return 400"

if __name__ == "__main__":
  test_build_query()
  test_build_query_error_query_string()
  test_build_query_error_empty_args()
  test_get_200()
  test_get_400()
  print("Everything passed")