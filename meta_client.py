from typing import List, Dict, Any

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights  # <- important

from config import META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN


def init_meta_api():
    FacebookAdsApi.init(
        app_id=META_APP_ID,
        app_secret=META_APP_SECRET,
        access_token=META_ACCESS_TOKEN,
    )


def get_account_insights(
    account_id: str,
    start_date: str,
    end_date: str,
) -> List[Dict[str, Any]]:
    """
    Fetch campaign level insights for a date range.
    """
    init_meta_api()

    account = AdAccount(account_id)

    params = {
        "time_range": {"since": start_date, "until": end_date},
        "level": "campaign",
        "time_increment": 1,
    }

    fields = [
        AdsInsights.Field.campaign_id,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.spend,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.actions,
        AdsInsights.Field.action_values,
        AdsInsights.Field.frequency,
    ]

    rows = account.get_insights(fields=fields, params=params)
    return [dict(r) for r in rows]
