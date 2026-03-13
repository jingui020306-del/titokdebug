from __future__ import annotations

from datetime import datetime
from typing import Literal

from app.schemas.common import ReportPreviewMixin

from pydantic import BaseModel, Field


class BenchmarkAccount(BaseModel):
    handle: str


class NicheInput(BaseModel):
    platform: Literal["抖音", "小红书"]
    niche_keyword: str
    goal: Literal["涨粉", "转咨询", "带货", "直播", "私域"]
    target_audience: str
    current_offer: str
    benchmark_accounts: list[BenchmarkAccount] = Field(..., min_length=3, max_length=10)
    current_stage: Literal["新号", "起量中", "老号重做"]
    risk_limits: str


class NicheMapReport(ReportPreviewMixin):
    job_id: str
    created_at: datetime
    niche_input: NicheInput
    market_summary: str
    audience_insights: list[str]
    competitor_layers: list[dict[str, str]]
    winning_formats: list[dict[str, str]]
    suggested_entry_points: list[str]
    avoid_directions: list[str]
    recommended_pillars: list[dict[str, str]]
    monetization_paths: list[str]
    recommended_next_step: Literal["go_rewrite_engine", "stay_in_niche_map", "back_to_account_audit"]


class NicheMapCreateResponse(BaseModel):
    job_id: str
    status: str
    message: str


class NicheMapHistoryItem(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    platform: str
    niche_keyword: str


class NicheMapHistoryResponse(BaseModel):
    items: list[NicheMapHistoryItem]


class NicheMapReportResponse(BaseModel):
    status: Literal["ready", "loading", "error"]
    data: NicheMapReport | None
