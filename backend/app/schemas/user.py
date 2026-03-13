from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UserProfile(BaseModel):
    id: str
    display_name: str
    email: str
    created_at: datetime


class AnalysisRecord(BaseModel):
    module: str
    job_id: str
    created_at: datetime
    status: str


class MeOverview(BaseModel):
    user: UserProfile
    account_audit_count: int
    niche_map_count: int
    rewrite_engine_count: int
    provider_mode: str
    last_analysis_at: datetime | None
    recent_records: list[AnalysisRecord]
