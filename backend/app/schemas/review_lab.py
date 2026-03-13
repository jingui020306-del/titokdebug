from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class BenchmarkAccountSummary(BaseModel):
    id: str
    user_id: str
    account_name: str
    platform: str
    account_url: str | None = None
    niche_label: str | None = None
    account_tier: Literal["head", "mid", "peer"]
    similarity_reason: str
    learnability_reason: str
    positioning_summary: str
    why_selected: str
    notes: str | None = None
    source_mode: Literal["manual", "discovered", "import"]
    created_at: datetime
    updated_at: datetime


class BenchmarkContentSample(BaseModel):
    id: str
    benchmark_account_id: str
    title: str
    sample_url: str | None = None
    content_type: str
    pillar_guess: str
    hook_style: str
    conversion_style: str
    sample_heat_level: Literal["normal", "strong", "viral"]
    sample_notes: str
    metrics_snapshot_text: str
    publish_date_text: str
    why_it_worked: str
    created_at: datetime
    updated_at: datetime


class BenchmarkPlaybook(BaseModel):
    id: str
    benchmark_account_id: str
    playbook_type: Literal["positioning", "profile", "pillar", "topic_selection", "hook", "delivery", "conversion_cta", "publishing_rhythm"]
    summary: str
    evidence_source: str
    confidence: int
    created_at: datetime
    updated_at: datetime


class BenchmarkGapItem(BaseModel):
    dimension: str
    my_current_state: str
    benchmark_state: str
    gap_level: Literal["low", "medium", "high"]
    why_gap_exists: str
    suggested_change: str
    urgency: Literal["now", "this_week", "later"]


class BenchmarkGapSummary(BaseModel):
    benchmark_account_id: str
    items: list[BenchmarkGapItem]


class AccountUpgradePlan(BaseModel):
    what_to_keep: list[str]
    what_to_change_now: list[str]
    what_to_change_later: list[str]
    what_not_to_copy: list[str]
    profile_upgrade_plan: list[str]
    content_structure_upgrade_plan: list[str]
    content_type_upgrade_plan: list[str]
    conversion_upgrade_plan: list[str]
    next_7_post_strategy: list[dict[str, str]]


class DiscoverySearchRequest(BaseModel):
    my_positioning: str
    niche_keyword: str
    goal: Literal["涨粉", "咨询", "直播"]
    target_audience: str
    content_style: str
    learning_preference: str


class DiscoveryCandidate(BaseModel):
    account_name: str
    platform: str
    account_url: str
    similarity_reason: str
    learnability_reason: str
    learn_target: str
    should_add: bool


class DiscoveryConfirmRequest(BaseModel):
    candidates: list[DiscoveryCandidate]


class BenchmarkCreateRequest(BaseModel):
    account_name: str
    platform: str = "抖音"
    account_url: str
    niche_label: str = "咨询型IP"
    account_tier: Literal["head", "mid", "peer"] = "peer"
    similarity_reason: str
    learnability_reason: str
    positioning_summary: str
    why_selected: str
    notes: str | None = None
    source_mode: Literal["manual", "discovered", "import"] = "manual"


class BenchmarkPatchRequest(BaseModel):
    notes: str | None = None
    why_selected: str | None = None
    account_tier: Literal["head", "mid", "peer"] | None = None


class BenchmarkSampleCreateRequest(BaseModel):
    title: str
    sample_url: str
    content_type: str
    pillar_guess: str
    hook_style: str
    conversion_style: str
    sample_heat_level: Literal["normal", "strong", "viral"] = "strong"
    sample_notes: str = ""
    metrics_snapshot_text: str = "公开数据样本"
    publish_date_text: str = "近期"
    why_it_worked: str = "结构清晰，承接明确"


class ReviewCreateRequest(BaseModel):
    source_type: Literal["manual", "authorized"]
    content_item_id: str | None = None
    publish_record_id: str | None = None
    version_id: str | None = None
    content_title: str
    publish_time: datetime
    content_pillar: str
    rewrite_version: str | None = None
    views: int
    likes: int
    comments: int
    favorites: int
    shares: int
    profile_visits: int
    dm_count: int = 0
    inquiry_count: int = 0
    conversion_count: int = 0
    consultation_count: int | None = None
    subjective_feedback: str | None = None


class ReviewReport(BaseModel):
    review_id: str
    created_at: datetime
    report_title: str
    preview_text: str
    recommended_next_module: Literal["positioning", "content_studio", "review_lab"]
    performance_summary: str
    self_comparison: str
    pillar_comparison: str
    benchmark_comparison: str
    best_account_playbook_match: str
    content_type_assessment: str
    consultation_performance_summary: str
    upgrade_progress_assessment: str
    decision: dict[str, str]
    next_iteration_actions: list[str]
    linked_content_context: dict[str, str]
    comparison_summary: str
    previous_version_comparison: dict[str, str | int | float]
    pillar_benchmark: dict[str, str | int | float | bool]
    strategy_window_comparison: dict[str, str | int | float]
    consultation_quality_signal: str
    conversion_readiness_assessment: str


class ReviewHistoryItem(BaseModel):
    review_id: str
    created_at: datetime
    content_title: str
    content_pillar: str
    major_metrics: str
    comparison_signal: str
    worth_scaling: str
    decision: str
    next_action: str
    pattern_impact: str
