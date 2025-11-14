from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import HealthCheckRequest, HealthCheckResponse
from meta_client import get_account_insights
from health_rules import aggregate_account_stats, detect_issues, build_summary

app = FastAPI(
    title="Meta Daily Health Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/meta/daily_health_check", response_model=HealthCheckResponse)
def daily_health_check(req: HealthCheckRequest):
    try:
        rows = get_account_insights(
            account_id=req.account_id,
            start_date=req.start_date,
            end_date=req.end_date,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No insights found.",
        )

    account_stats = aggregate_account_stats(rows)
    issues = detect_issues(rows)
    summary = build_summary(account_stats, issues)

    return HealthCheckResponse(
        summary=summary,
        account_stats=account_stats,
        issues=issues,
    )
