from typing import List, Dict, Any
from models import AccountStats, Issue

def _safe_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0

def aggregate_account_stats(rows: List[Dict[str, Any]]) -> AccountStats:
    total_spend = sum(_safe_float(r.get("spend", 0)) for r in rows)
    total_impressions = sum(int(r.get("impressions", 0)) for r in rows)
    total_clicks = sum(int(r.get("clicks", 0)) for r in rows)

    ctr = (total_clicks / total_impressions) if total_impressions else 0.0
    cpc = (total_spend / total_clicks) if total_clicks else 0.0

    total_results = 0.0
    for r in rows:
        actions = r.get("actions") or []
        for a in actions:
            if a.get("action_type") in ("purchase", "lead", "complete_registration"):
                total_results += _safe_float(a.get("value", 0))

    cpr = (total_spend / total_results) if total_results else 0.0

    return AccountStats(
        spend=round(total_spend, 2),
        impressions=total_impressions,
        clicks=total_clicks,
        ctr=ctr,
        cpc=round(cpc, 4) if cpc else 0.0,
        results=total_results or None,
        cpr=round(cpr, 2) if cpr else None,
    )

def detect_issues(rows: List[Dict[str, Any]]) -> List[Issue]:
    issues: List[Issue] = []

    MIN_CTR = 0.01
    MAX_CPC = 1.50
    MAX_FREQUENCY = 5.0
    MIN_SPEND_TO_JUDGE = 20.0

    for r in rows:
        cid = r.get("campaign_id", "")
        cname = r.get("campaign_name", "Unnamed campaign")
        spend = _safe_float(r.get("spend", 0))
        impressions = int(r.get("impressions", 0))
        clicks = int(r.get("clicks", 0))
        freq = _safe_float(r.get("frequency", 0))

        if spend < MIN_SPEND_TO_JUDGE:
            continue

        ctr = (clicks / impressions) if impressions else 0.0
        ctr_pct = ctr * 100
        cpc = (spend / clicks) if clicks else 0.0

        if ctr < MIN_CTR:
            issues.append(Issue(
                level="high",
                campaign_id=cid,
                campaign_name=cname,
                metric="CTR (%)",
                value=round(ctr_pct, 2),
                benchmark=MIN_CTR * 100,
                reason="CTR is lower than the normal range.",
                suggestion="Update primary text and test new visuals.",
            ))

        if cpc > MAX_CPC:
            issues.append(Issue(
                level="medium",
                campaign_id=cid,
                campaign_name=cname,
                metric="CPC",
                value=round(cpc, 4),
                benchmark=MAX_CPC,
                reason="Cost per click is high.",
                suggestion="Try broader audiences or cheaper placements.",
            ))

        if freq > MAX_FREQUENCY:
            issues.append(Issue(
                level="medium",
                campaign_id=cid,
                campaign_name=cname,
                metric="Frequency",
                value=round(freq, 2),
                benchmark=MAX_FREQUENCY,
                reason="Ad is being shown too many times.",
                suggestion="Rotate new creatives or reduce budget.",
            ))

    return issues

def build_summary(account_stats: AccountStats, issues: List[Issue]) -> str:
    if not issues:
        return (
            f"Healthy account. Spend RM{account_stats.spend:.2f}, "
            f"{account_stats.impressions} impressions, {account_stats.clicks} clicks."
        )

    high = sum(1 for i in issues if i.level == "high")
    med = sum(1 for i in issues if i.level == "medium")

    return (
        f"Found {len(issues)} issues "
        f"({high} high, {med} medium). "
        f"Total spend RM{account_stats.spend:.2f}."
    )
