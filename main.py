from helper.facebook import Facebook
from dataframe.facebook_insight import FacebookInsight
from utils.database import Database
import sys

if __name__ == "__main__":
    facebook = Facebook()
    facebook.set_token("EAAEpE5CoeZC8BAJXpwIw4KgjWhqNs2Bml4EyYJAfTW51qSjzMrTygsZB5yKKGbgi8E2FHzISEQaRNQbsX8ejyOJ84oVL9N4m5E0dkG6oX1I7CbhezcVRZCGZCTKpywnAIXemOvUfxLweH2BNJOnLNepodRqpQutVaA8KEDXs6QZDZD")
    if not facebook.is_token_valid():
        sys.exit("Token is invalid")

    facebook.set_account("act_2563373910645150")
    facebook.set_level("campaign")
    facebook.set_field("campaign_name,impressions,reach,inline_link_clicks,ctr,cpc,spend,purchase_roas,actions")

    insights = facebook.get_insight(since="2021-07-04", until="2021-07-10").json()
    data = FacebookInsight(insights["data"])

    data["roas"] = data.get_action("purchase_roas", "omni_purchase")
    data["purchase"] = data.get_action("actions", "purchase")
    data["revenue"] = data['roas'].astype(float) * data["spend"].astype(float)

    filtered = data.reindex(columns=["date_start", "campaign_name", "impressions", "reach", "inline_link_clicks", "ctr", "cpc", "spend", "roas", "purchase", "revenue"])
    output = filtered.rename(columns={"date_start": "date", "campaign_name": "name", "inline_link_clicks": "clicks"}, errors="raise")

    connection = Database(database="example").initialize()

    output.to_sql("demo", con=connection, if_exists="append", index=False)

    print(output)