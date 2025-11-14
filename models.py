from pydantic import BaseModel
from typing import List, Optional

class HealthCheckRequest(BaseModel):
    account_id: str
    start_date: str   # ISO date: "2025-11-01"
    end_date: str     # ISO date

class AccountStats(BaseModel):
    spend: float
    impressions: int
    clicks: int
    ctr: float
    cpc: float
    results: Optional[float] = None
    cpr: Optional[float] = None

class Issue(BaseModel):
    level: str
    campaign_id: str
    campaign_name: str
    metric: str
    value: float
    benchmark: Optional[float] = None
    reason: str
    suggestion: str

class HealthCheckResponse(BaseModel):
    summary: str
    account_stats: AccountStats
    issues: List[Issue]
