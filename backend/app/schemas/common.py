from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None
    meta: dict[str, Any] | None = None


class ReportSummary(BaseModel):
    id: str
    title: str
    preview_text: str
    created_at: datetime


class HistoryItem(BaseModel):
    id: str
    title: str
    status: str
    created_at: datetime


class TodoItem(BaseModel):
    id: str
    user_id: str
    title: str
    source_module: Literal["positioning", "content_studio", "review_lab", "workspace"]
    source_report_id: str | None = None
    priority: Literal["high", "medium", "low"] = "medium"
    status: Literal["todo", "in_progress", "paused", "done"] = "todo"
    action_type: Literal["rewrite_profile", "generate_weekly_plan", "rewrite_single_post", "fill_review", "scale_pillar", "stop_direction"]
    suggested_due_label: str = "本周"
    created_at: datetime
    updated_at: datetime


class PatternItem(BaseModel):
    id: str
    user_id: str
    pattern_type: Literal["title_style", "hook_style", "pillar", "profile_expression", "conversion_cta", "risk_direction"]
    label: str
    summary: str
    evidence_source: str
    confidence: int = Field(ge=0, le=100)
    current_status: Literal["candidate", "validated", "deprecated"]
    created_at: datetime
    updated_at: datetime


class TimelineItem(BaseModel):
    id: str
    event_type: str
    title: str
    summary: str
    created_at: datetime


class ContentItemSummary(BaseModel):
    id: str
    title_or_working_title: str
    pillar: str
    content_goal: str
    status: Literal["planned", "drafted", "adopted", "published", "reviewed", "archived"]
    chosen_version_id: str | None = None
    latest_publish_record_id: str | None = None
    latest_review_id: str | None = None
    updated_at: datetime


class ContentVersionSummary(BaseModel):
    id: str
    content_item_id: str
    version_label: str
    title: str
    hook: str
    is_adopted: bool
    created_at: datetime


class PublishRecordSummary(BaseModel):
    id: str
    content_item_id: str
    version_id: str | None
    platform: str
    published_at: datetime
    views: int
    inquiry_count: int
    conversion_count: int


class ConsultationPerformanceSummary(BaseModel):
    dm_count: int
    inquiry_count: int
    conversion_count: int
    summary: str


class ReviewComparisonSummary(BaseModel):
    comparison_summary: str
    previous_version_comparison: dict[str, Any]
    pillar_benchmark: dict[str, Any]
    strategy_window_comparison: dict[str, Any]


class PositioningVersionSummary(BaseModel):
    positioning_version_id: str
    job_id: str
    report_title: str
    preview_text: str
    is_active: bool
    is_frozen: bool
    frozen_at: datetime | None = None
    supersedes_version_id: str | None = None
    change_level: Literal["minor", "moderate", "major"]
    created_at: datetime


class WorkflowRecommendationSummary(BaseModel):
    current_workflow_stage: str
    best_next_action: str
    best_next_action_reason: str


class ReportPreviewMixin(BaseModel):
    report_title: str
    preview_text: str
    recommended_next_module: Literal["account_audit", "niche_map", "rewrite_engine", "positioning", "content_studio", "review_lab"]
