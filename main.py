from helper.facebook import Facebook
import sys

if __name__ == "__main__":
    facebook = Facebook()
    facebook.set_token("EAABsbCS1iHgBAFwJHsJRLyeYs4HUSYjGX8cn11cl6ZCQevAcOVNW7Gfv3T5Qfwf1CcYYo4rHCloRf6jaDiVFecfwbzEZCzRu9ZBV5k2Uq5bBbEFY4NFc0LkvGZCfYqNeUZB3nozMQkAKGjZCnE5MajJdxv7yji260wZBSu0lgyvWAZDZD")
    facebook.set_account("act_2563373910645150")
    facebook.set_level("campaign")
    facebook.set_field("campaign_name,impressions,reach,inline_link_clicks,ctr,cpc,spend,purchase_roas,actions")
    if not facebook.is_token_valid():
        sys.exit("Token is invalid")
    print(facebook.get_insight(since="2021-07-04", until="2021-07-10").text)