#-*- coding: euc-kr -*-
'''
Created on 2016. 8. 31.

@author: psyoblade
'''
import datetime
import os
from tune_reporting.api import AdvertiserReportActuals
from tune_reporting import SdkConfig

week_ago = datetime.date.fromordinal(datetime.date.today().toordinal() - 8)
yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)
start_date = "{} 00:00:00".format(week_ago)
end_date = "{} 23:59:59".format(yesterday)
dirname = os.path.split(__file__)[0]
dirname = os.path.dirname(dirname)
filepath = os.path.join(dirname, "config", SdkConfig.SDK_CONFIG_FILENAME)
abspath = os.path.abspath(filepath)
sdk_config = SdkConfig(filepath=abspath)
advertiser_report = AdvertiserReportActuals()

def direct_success():
    import requests
    find='https://api.mobileapptracking.com/v2/advertiser/stats/find.json?api_key=' + sdk_config.auth_key + '&start_date=2016-08-30+00%3A00%3A00+&end_date=2016-08-30+00%3A00%3A00+&filter=(debug_mode+%3D+0)+AND+(test_profile_id+%3D+0)&fields[]=site_id&fields[]=site.name&fields[]=publisher_id&fields[]=publisher.name&fields[]=ad_clicks&fields[]=ad_clicks_unique&fields[]=installs&fields[]=campaign_id&fields[]=campaign.name&group[]=publisher_id'
    r = requests.get(find)
    if r.status_code == 200:
        data = r.json().get("data")
        for r in data:
            print "AppName:%s, Partner:%s, Campaign: %s, DailyClick:%s, DailyInstall:%s" % (r["site"]["name"], r["publisher"]["name"], r["campaign"]["name"], r["ad_clicks"], r["installs"])
            break
    else:
        print "Failure"

def count_success():
    map_params = {
                "start_date": start_date,
                "end_date": end_date,
                "filter": "(publisher_id > 0)",
                "group": "site_id,publisher_id",
                "response_timezone": "America/Los_Angeles"
            }
    response = advertiser_report.count(
        map_params
    )
    if response.http_code != 200 or response.errors:
        raise Exception("Failed: {}: {}".format(response.http_code, str(response)))

    print(" TuneServiceResponse:")
    print(str(response))

def find_failure():
    map_params = {
        "start_date": start_date,
        "end_date": end_date,
        "fields": None,
        "filter": "(publisher_id > 0)",
        "group": "site_id,publisher_id",
        "limit": 5,
        "page": None,
        "sort": {"paid_installs": "DESC"},
        "timestamp": "datehour",
        "response_timezone": "America/Los_Angeles"
    }

    response = advertiser_report.find(
        map_params
    )

    if response.http_code != 200 or response.errors:
        raise Exception("Failed: {}: {}".format(response.http_code, str(response)))

    print(" TuneServiceResponse:")
    print(str(response))


def main():
#     direct_success()
#     count_success()
    find_failure()

if __name__ == "__main__":
    main()
