from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class ActivePositioningSnapshot(BaseModel):
    has_active: bool
    has_frozen: bool
    preview_text: str


class ContentItemSnapshot(BaseModel):
    id: str
    pillar: str
    status: str


class ContentVersionSnapshot(BaseModel):
    id: str
    content_item_id: str
    version_label: str
    created_at: datetime


class PublishRecordSnapshot(BaseModel):
    id: str
    content_item_id: str
    published_at: datetime
    views: int
    likes: int
    comments: int
    favorites: int
    shares: int
    profile_visits: int
    dm_count: int
    inquiry_count: int
    conversion_count: int


class ReviewEntrySnapshot(BaseModel):
    id: str
    created_at: datetime
    decision: str
    bottleneck_stage: str
    next_action: str


class LearnedPatternSnapshot(BaseModel):
    id: str
    pattern_type: str
    label: str
    summary: str
    confidence: int
    current_status: Literal["candidate", "validated", "deprecated"]


class BenchmarkAccountSnapshot(BaseModel):
    id: str
    account_name: str
    account_tier: str
    similarity_reason: str
    learnability_reason: str
    why_selected: str


class BenchmarkContentSampleSnapshot(BaseModel):
    id: str
    benchmark_account_id: str
    title: str
    content_type: str
    pillar_guess: str
    sample_heat_level: str


class TodoItemSnapshot(BaseModel):
    id: str
    title: str
    source_module: str
    priority: str
    status: str
    action_type: str


class IntegrationStatusSnapshot(BaseModel):
    douyin_connected: bool
    oauth_mode: str


class UserGrowthSnapshot(BaseModel):
    user_id: str
    active_positioning: ActivePositioningSnapshot
    frozen_positioning: bool
    content_pillars: list[str]
    recent_content_items: list[ContentItemSnapshot]
    recent_versions: list[ContentVersionSnapshot]
    publish_records: list[PublishRecordSnapshot]
    recent_reviews: list[ReviewEntrySnapshot]
    learned_patterns: list[LearnedPatternSnapshot]
    benchmark_accounts: list[BenchmarkAccountSnapshot]
    benchmark_samples: list[BenchmarkContentSampleSnapshot]
    todo_items: list[TodoItemSnapshot]
    account_goal: str
    current_stage_hint: str | None = None
    integration_status: IntegrationStatusSnapshot
