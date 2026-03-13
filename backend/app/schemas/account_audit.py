from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ReportStatus = Literal["loading", "ready", "insufficient-data", "permission-insufficient", "error"]
JobSourceType = Literal["mock", "oauth"]
JobStatus = Literal["created", "syncing_fast", "fast_ready", "syncing_deep", "deep_ready", "failed"]


class AccountProfile(BaseModel):
    account_id: str = Field(..., description="账号唯一标识")
    nickname: str
    category: str
    city: str
    followers: int
    following: int
    bio: str


class AccountMetrics(BaseModel):
    post_count_30d: int
    avg_views_30d: int
    avg_completion_rate_30d: float
    avg_interaction_rate_30d: float
    follow_convert_rate_30d: float


class PostSnapshot(BaseModel):
    post_id: str
    title: str
    topic: str
    views: int
    likes: int
    comments: int
    shares: int
    publish_time: datetime


class ScoreItem(BaseModel):
    name: Literal["定位清晰度", "主页信任感", "内容一致性", "内容吸附力", "转化承接力", "风险暴露度"]
    score: int = Field(..., ge=0, le=100)
    reason: str


class IssueItem(BaseModel):
    issue: str
    severity: Literal["low", "medium", "high"]
    evidence: str


class ActionItem(BaseModel):
    phase: Literal["7d", "30d", "60d"]
    action: str
    expected_outcome: str


class RoutingDecision(BaseModel):
    recommended_module: Literal["account-audit", "niche-map", "rewrite-engine"]
    reason: str
    next_step: str


class ProfileRewriteSuggestions(BaseModel):
    nickname_suggestion: str
    bio_suggestion: str
    profile_positioning_statement: str


class ContentPillarItem(BaseModel):
    pillar: str
    why: str
    suitable_audience: str


class DayActionItem(BaseModel):
    day: Literal["day1", "day2", "day3", "day4", "day5", "day6", "day7"]
    action: str


class FastReport(BaseModel):
    job_id: str
    generated_at: datetime
    account_profile: AccountProfile
    account_metrics: AccountMetrics
    post_snapshots: list[PostSnapshot]
    summary: str
    report_title: str
    preview_text: str
    executive_summary: str
    scores: list[ScoreItem]
    top_issues: list[IssueItem]
    profile_diagnosis: dict[str, str]
    content_diagnosis: dict[str, str]
    growth_bottleneck: dict[str, str]
    bottleneck_explanation: str
    risk_alerts: list[str]
    action_plan: list[ActionItem]
    profile_rewrite_suggestions: ProfileRewriteSuggestions
    content_pillars: list[ContentPillarItem]
    seven_day_action_plan: list[DayActionItem]
    avoid_now: list[str]
    recommended_next_module: Literal["niche_map", "rewrite_engine", "stay_in_account_audit"]
    routing: RoutingDecision


class DeepReport(FastReport):
    deep_insight: dict[str, str]
    benchmark_hint: dict[str, str]


class MockCreateRequest(BaseModel):
    account_id: str
    nickname: str = "未命名创作者"
    category: str = "知识分享"
    city: str = "杭州"
    source_type: JobSourceType = "mock"


class MockCreateResponse(BaseModel):
    job_id: str
    status: str
    message: str


class SupplementRequest(BaseModel):
    goal: str
    target_audience: str
    monetization_mode: str


class FastReportResponse(BaseModel):
    status: ReportStatus
    message: str
    data: FastReport | None = None


class DeepReportResponse(BaseModel):
    status: ReportStatus
    message: str
    data: DeepReport | None = None


class AccountAuditJobItem(BaseModel):
    id: str
    source_type: JobSourceType
    status: JobStatus
    report_mode_available: list[Literal["fast", "deep"]]
    created_at: datetime
    updated_at: datetime


class AccountAuditHistoryItem(AccountAuditJobItem):
    account_nickname: str


class AccountAuditHistoryResponse(BaseModel):
    items: list[AccountAuditHistoryItem]


class AccountAuditJobStatusResponse(BaseModel):
    data: AccountAuditJobItem


class AccountAuditReportsResponse(BaseModel):
    job_id: str
    reports: list[dict[str, str | int]]
