from dataframe.facebook_insight import FacebookInsight
import sqlalchemy
import pandas as pd

if __name__ == "__main__":
    data = FacebookInsight(pd.read_json("test/facebook_insight_payload.json"))

    data["roas"] = data.get_action("purchase_roas", "omni_purchase")
    data["purchase"] = data.get_action("actions", "purchase")
    data["revenue"] = data['roas'].astype(float) * data["spend"].astype(float)

    filtered = data.reindex(columns=["date_start", "campaign_name", "impressions", "reach", "inline_link_clicks", "ctr", "cpc", "spend", "roas", "purchase", "revenue"])
    output = filtered.rename(columns={"date_start": "date", "campaign_name": "name", "inline_link_clicks": "clicks"}, errors="raise")

    connection = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/example')

    output.to_sql("demo", con=connection, if_exists="append", index=False)