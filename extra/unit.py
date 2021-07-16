#!/usr/bin/env python
#
# Copyright 2020 Advertize.net All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import pytz
import locale
import _locale
import pandas as pd
from io import StringIO
from config import *
from datetime import datetime
from datetime import timedelta
from neg_utilities import Utilities
from neg_adwords import AdwordsClient

adwords_client = AdwordsClient()
util = Utilities()

account_id = '965-394-4858' # Proof
report_variants = ['NEAR_EXACT', 'NEAR_PHRASE']

adwords_client.set_account(account_id, util, 'ProofAudit')

def testpass(msg):
  print(msg + ': PASSED')

def test_remove_emoji():
  str_emoji = '™️Trade Mark'
  new_str = util.remove_emoji(str_emoji)
  assert str_emoji != new_str, "Should be ™️Trade Mark => Trade Mark"
  testpass('] test_remove_emoji')

def test_remove_no_emoji():
  str_emoji = 'Trade Mark'
  new_str = util.remove_emoji(str_emoji)
  assert str_emoji == new_str, "Nothing should have change"
  testpass('] test_remove_no_emoji')

def test_path_report_creator():
  path_str = util.get_file_path(ftype = 'testdir', account_name = 'proof')
  assert 'testdir' in path_str and 'proof' in path_str, "Path creator returns invalid structure"
  print(path_str)
  testpass('] test_path_report_creator')

def test_path_report_invalid_creator():
  path_str = util.get_file_path(ftype = 'testdir', account_name = 'proof')
  assert 'testdir ' not in path_str and 'Xproof' not in path_str, "Path creator should not return testdir<spance> & Xproof"
  print(path_str)
  testpass('] test_path_report_invalid_creator')

def test_timezone():
  assert util.get_timestamp() != datetime.now(pytz.timezone(TIMEZONE)), "Timezones does not match"
  testpass('] test_timezone')

def test_mm2_campaign_parser_complete():
  campaign_name = 'AN/NB/Frost/Master/female+/mct/token1/phrase 10%'
  p = util.parse_campaign(campaign_name)
  is_match = (
    p['prefix'] == 'AN/NB/Frost' and 
    p['role'] == 'master' and 
    p['match'] == 'phrase' and 
    p['gender'] == 'female|unknown'  and 
    p['device'] == 'mobile|computer|tablet'  and 
    p['suffix'] == ['10%'] and 
    p['unknown_tokens'] == ['token1']
  )
  assert is_match, "MM2 parser failed to output expected result"
  testpass('] test_mm2_campaign_parser_complete')
  print(campaign_name)
  print(p)
  print()

def test_mm2_campaign_failed_parser_complete():
  campaign_name = 'AN/Proof/Frost/Master/female+/mct/phrase 20%'
  p = util.parse_campaign(campaign_name)
  is_match = (
    p['prefix'] != 'an/nb/frost1' and 
    p['role'] == 'master' and 
    p['match'] == 'phrase' and 
    p['gender'] == 'female|unknown'  and 
    p['device'] != 'mobile|computertablet'  and 
    p['suffix'] == ['20%'] and 
    p['unknown_tokens'] == []
  )
  assert is_match, "MM2 parser failed to output expected result"
  testpass('] test_mm2_campaign_failed_parser_complete')
  print(campaign_name)
  print(p)
  print()

def test_mm2_campaign_no_parse():
  campaign_name = 'Random String Campaing Name'
  p = util.parse_campaign(campaign_name)
  assert p == None, "MM2 parser did not return None"
  testpass('] test_mm2_campaign_no_parse')
  print(campaign_name)
  print(p)
  print()

def test_mm2_campaign_token_parser():
  campaign_name = 'AN/BB/Frost/Master/female/token1/token2/mct/token3/phrase 20%'
  p = util.parse_campaign(campaign_name)
  assert p['unknown_tokens'] == ['token1', 'token2', 'token3'], "MM2 parser token did not match"
  testpass('] test_mm2_campaign_token_parser')
  print(campaign_name)
  print(p['unknown_tokens'])
  print()

def test_mm2_campaign_no_token_parser():
  campaign_name = 'AN/BB/Frost/Master/female/mct/phrase 40%'
  p = util.parse_campaign(campaign_name)
  assert p['unknown_tokens'] == [], "MM2 parser token should be empty"
  testpass('] test_mm2_campaign_no_token_parser')
  print(campaign_name)
  print(p['unknown_tokens'])
  print()

def test_search_term_report():
  try:
    search_terms = adwords_client.get_search_term_report(
      save_to_file = False,
      report_variants = report_variants
    )
  except Exception as identifier:
    assert False, identifier

  sts = pd.read_csv(StringIO(search_terms), delimiter=',')
  assert not sts.empty , "Search terms should not be empty"
  testpass('] test_search_term_report')
  print(sts)
  print("AW SearchTerms Report Normal")
  print()

def test_pull_positive_kw_adgroups_only():
  try:
    poskw = adwords_client.get_keywords_report(save_to_file = False, match_type=['EXACT', 'PHRASE'])
  except Exception as identifier:
    assert False, identifier
  
  sts = pd.read_csv(StringIO(poskw), delimiter=',')
  assert not sts.empty , "Positive Keywords should not be empty"
  
  print()
  print('Checking if postive report are really positive...')
  kws = sts['Is negative'].to_numpy()
  for kw in kws:
    assert kw == False, "VERY CRITICAL: There are negative keywords!"

  print(sts)
  testpass('] test_pull_positive_kw_adgroups_only')
  print("AW Positive Keyword Report Normal")

def test_exact_phrase_campaign_adgroups_only():
  try:
    raw = adwords_client.get_adgroups(return_key = 'Campaign')
  except Exception as identifier:
    assert False, identifier
  
  print('List of AdGroups was pull without exceptions...')

  assert 'EXACT' in raw and 'PHRASE' in raw, "AdGroup response structure not valid"
  print(raw)
  print()
  print('AdGroup response structure valid')

  print()
  print('Checking AdGroup CAMPAIGNS are really MM2 Exact or Phrase...')
  for e in raw['EXACT']:
    print(e)
    assert 'exact' in e.lower(), "VERY CRITICAL: none MM2 EXACT was catch!" + str(e)

  for p in raw['PHRASE']:
    print(p)
    assert 'phrase' in p.lower(), "VERY CRITICAL: none MM2 PHRASE was catch!" + str(p)

  print()
  print('AdGroup CAMPAIGNS are really MM2 Exact/Phrase')
  print()
  testpass('] test_exact_phrase_campaign_adgroups_only')

def test_generate_negative_keywords_complete_operations():
  print()
  print('Checking complete workflow....')
  print()
  print('Pulling search terms')
  try:
    search_terms = adwords_client.get_search_term_report(
      save_to_file = False,
      report_variants = report_variants
    )
  except Exception as identifier:
    assert False, identifier
  print('Pulling search terms - Normal')
  print()
  print('Pulling positive keywords')
  try:
    postive_keywords = adwords_client.get_keywords_report(save_to_file = False, match_type=['EXACT', 'PHRASE'])
  except Exception as identifier:
    assert False, identifier
  print('Pulling positive keywords - Normal')
  print()
  print('Pulling adgroups')
  try:
    adgroups = adwords_client.get_adgroups(return_key = 'Ad group ID')
  except Exception as identifier:
    assert False, identifier
  print('Pulling positive keywords - Normal')
  print()
  print('Checking EXACT negs kw...')
  for adgroup_id_exact in adgroups['EXACT']:
    try:
      negative_keywords_e = adwords_client.generate_adgroup_negative_keywords(
        adgroup_id = adgroup_id_exact, match_type = 'EXACT',
        search_terms = search_terms, postive_keywords = postive_keywords
      )
      if len(negative_keywords_e):
        print(negative_keywords_e)
        for nge in negative_keywords_e:
          assert nge['adGroupId'] == adgroup_id_exact, "VERY CRITICAL: This adgroup id should be existed here: " + str(nge['adGroupId'])

    except Exception as identifier:
      assert False, identifier
  print()
  print('Checking PHRASE negs kw...')
  for adgroup_id_phrase in adgroups['PHRASE']:
    try:
      negative_keywords_p = adwords_client.generate_adgroup_negative_keywords(
        adgroup_id = adgroup_id_phrase, match_type = 'PHRASE',
        search_terms = search_terms, postive_keywords = postive_keywords
      )
      if len(negative_keywords_p):
        print(negative_keywords_p)
        for ngp in negative_keywords_p:
          assert ngp['adGroupId'] == adgroup_id_phrase, "VERY CRITICAL: This adgroup id should be existed here: " + str(ngp['adGroupId'])

    except Exception as identifier:
      assert False, identifier

  testpass('] test_generate_negative_keywords_complete_operations')
  print()
  print('All negkw operations are normal.')

if __name__ == "__main__":
  old_stdout = sys.stdout
  new_stdout = StringIO()
  sys.stdout = new_stdout
  print(util.get_timestamp())
  print()
  print('*** Functional Tests ***')
  print()
  test_remove_emoji()
  test_remove_no_emoji()
  test_path_report_creator()
  test_path_report_invalid_creator()
  test_timezone()
  print()
  print('*** MM2 Tests ***')
  print()
  test_mm2_campaign_parser_complete()
  test_mm2_campaign_failed_parser_complete()
  test_mm2_campaign_no_parse()
  test_mm2_campaign_token_parser()
  test_mm2_campaign_no_token_parser()
  print()
  print('*** Adwords Tests ***')
  print()
  test_search_term_report()
  test_pull_positive_kw_adgroups_only()
  test_exact_phrase_campaign_adgroups_only()
  test_generate_negative_keywords_complete_operations()
  print()
  print("Everything passed")
  output = new_stdout.getvalue()
  sys.stdout = old_stdout

  util.save_to_file(file_name = UNIT_LOG, file_contents = output)
  test_result = '[PASSED] '

  if 'Everything passed' not in output:
    test_result = '[FAILED!!!] '

  util.send_generic_email(
    subject = 'NegKW Test - ' + test_result + str(datetime.now(pytz.timezone(TIMEZONE))), 
    body = 'Attached: NegKW Test result file. Please do not reply.',
    file = UNIT_LOG
  )