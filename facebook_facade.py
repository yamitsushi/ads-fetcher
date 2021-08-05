from helper.facebook import Facebook
from dataframe.facebook_insight import FacebookInsight
from utils.database import Database
import sys

def facebook_facade():
    facebook = Facebook()
    facebook.set_token("EAAEpE5CoeZC8BAOSq1MBHOADyoRXf8FZB1ngypU36ZByEOy9ZAzjulfhZAVEft8DPnTSJBZAZBo0SL1ObJjDIyFF3hn52zZBsDVm91LK9g8pJZCrsbXZAbURrZA1nFmQHBtJgteCp1XX1C0q4wA9QOlcv7l0kMV80zyJ4mVouEcDUxSAJ2SNjcxCeLp")
    if not facebook.is_token_valid():
        sys.exit("Token is invalid")

    facebook.set_account("act_2563373910645150")
    facebook.set_level("campaign")
    facebook.set_field("campaign_name,impressions,reach,inline_link_clicks,ctr,cpc,spend,purchase_roas,actions")

    insights = facebook.get_insight(since="2021-07-04", until="2021-07-10").json()
    data = FacebookInsight(insights["data"])
    data = data.sort(column_name='campaign_name', ascending=True)

    data["roas"] = data.get_action("purchase_roas", "omni_purchase")
    data["purchase"] = data.get_action("actions", "purchase")
    data["revenue"] = data['roas'].astype(float) * data["spend"].astype(float)

    filtered = data.reindex(columns=["date_start", "campaign_name", "impressions", "reach", "inline_link_clicks", "ctr", "cpc", "spend", "roas", "purchase", "revenue"])
    output = filtered.rename(columns={"date_start": "date", "campaign_name": "name", "inline_link_clicks": "clicks"}, errors="raise")

    connection = Database(database="example").initialize()

    output.to_sql("demo", con=connection, if_exists="append", index=False)

    print(output)