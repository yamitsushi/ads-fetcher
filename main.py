from helper.facebook import Facebook
import sys

if __name__ == "__main__":
    facebook = Facebook()
    facebook.set_token("EAAEpE5CoeZC8BAP29q1ACdexY195b4cpg0kXos6LUDgk6T1o6l1GuaBx2zs0tRr5YbZAKECoiBIbN2jktr56EDG4XfjynAG6G5H5lEQpYz4f6Y4vBgUd0xoSftvKGorH5Dn2aLxFBUOWbaMmbv8aigsyhaAU3Qf3iuwJIQhaSakbO1gG9Uort2tBXWyxYZD")
    facebook.set_account("act_2563373910645150")
    facebook.set_level("campaign")
    facebook.set_field("campaign_name,impressions,reach,inline_link_clicks,ctr,cpc,spend,purchase_roas,actions")
    if not facebook.is_token_valid():
        sys.exit("Token is invalid")
    print(facebook.get_insight(since="2021-07-04", until="2021-07-10").text)