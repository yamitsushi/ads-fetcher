from helper.facebook import Facebook
from dataframe.facebook_insight import FacebookInsight
import sys

if __name__ == "__main__":
    facebook = Facebook()
    facebook.set_token("EAABsbCS1iHgBAJhPrFK2xEfAVVVQ5dSl7IDr1cNvTuFZBWTa1WTnY47G1t9ZB0VvXg7vCv8B1d9Cr9CX17x2G9C1Mhrp8FbR46vsFZCr6vs9smjl0Y0iqleCXH2sZC7mXJdB4iEY3jZATBqp7wfY6Wo5ZBd3Mosc91foLjl7aYQwZDZD")
    facebook.set_account("act_2563373910645150")
    facebook.set_level("campaign")
    facebook.set_field("campaign_name,impressions,reach,inline_link_clicks,ctr,cpc,spend,purchase_roas,actions")
    if not facebook.is_token_valid():
        sys.exit("Token is invalid")
    insights = facebook.get_insight(since="2021-07-04", until="2021-07-10").json()

    data = FacebookInsight(insights["data"])

    data.get_roas("roas")
    data.get_purchase("purchase")
    data.get_revenue("revenue")
    limit = data.limit(["date_start", "campaign_name", "impressions", "reach", "inline_link_clicks", "ctr", "cpc", "spend", "roas", "purchase", "revenue"])
    output = limit.rename(columns={"date_start": "date", "campaign_name": "name", "inline_link_clicks": "clicks"}, errors="raise")
    print(output)