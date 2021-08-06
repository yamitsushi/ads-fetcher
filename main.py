from facebook_facade import facebook_facade

from googleads import adwords
import pandas as pd

import sys

if __name__ == "__main__":
    # facebook_facade()
    

    client = adwords.AdWordsClient.LoadFromStorage("config/googleads.yaml")
    client.SetClientCustomerId("965-394-4858")


    report_downloader = client.GetReportDownloader()

    report_query = (adwords.ReportQueryBuilder()
      .Select('CampaignId','CampaignName')
      .From('CAMPAIGN_PERFORMANCE_REPORT')
      .Build())

    response = report_downloader.DownloadReportAsStreamWithAwql(
      report_query, 
      'CSV', 
      skip_report_header=True,
      skip_column_header=False,
      skip_report_summary=True
    )
    data = pd.read_csv(response)
    print(data)
    sys.exit("Program Completed")