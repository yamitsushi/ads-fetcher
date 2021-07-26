from helper.facebook import Facebook
from dataframe.facebook_insight import FacebookInsight
import sys

if __name__ == "__main__":
    facebook = Facebook()
    facebook.set_token("EAABsbCS1iHgBAKudwQUurM4W6MTWEAdTqrWmTayWsZBGTlXjZCX3GV8uWhpQkwZB5WYwtaPcAMBfq7HaRHI3wOGZBlfSZCTsTE8qtT8v812TrF881apUDe9phWGIVbRwKMdnLL4nXSxN0oVJx68eiLLYMH7iPMYPRkMS541lTkwZDZD")
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

    filtered = data.filter("date_start", "campaign_name", "impressions", "reach", "inline_link_clicks", "ctr", "cpc", "spend", "roas", "purchase", "revenue")
    output = filtered.rename(columns={"date_start": "date", "campaign_name": "name", "inline_link_clicks": "clicks"}, errors="raise")

    print(output)