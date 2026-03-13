from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.schemas.common import ContentItemSummary, ContentVersionSummary, PublishRecordSummary, TimelineItem


class WeeklyPlanRequest(BaseModel):
    one_line_positioning: str
    content_pillars: list[str]
    target_audience_summary: str
    weekly_goal: Literal["涨粉", "转咨询", "直播预热", "私域承接"]
    posts_per_week: int = 7
    has_live: bool = False
    primary_service: str


class WeeklyPlanReport(BaseModel):
    plan_id: str
    created_at: datetime
    report_title: str
    preview_text: str
    recommended_next_module: Literal["content_studio", "review_lab", "positioning"]
    weekly_strategy_summary: str
    content_calendar: list[dict[str, str | bool]]
    pillar_distribution: list[dict[str, str | int]]
    live_topic_suggestions: list[str]
    consultation_conversion_posts: list[str]
    high_risk_topics_to_avoid: list[str]


class ContentRewriteRequest(BaseModel):
    platform: Literal["抖音", "小红书"]
    goal_action: str
    original_title: str
    original_script: str
    original_cover_text: str
    pillar: str
    risk_limits: list[str]
    target_audience: str
    content_item_id: str | None = None


class ContentHistoryItem(BaseModel):
    id: str
    kind: Literal["weekly_plan", "rewrite"]
    created_at: datetime
    title: str
    status: str


class ContentItemDetail(BaseModel):
    item: ContentItemSummary
    chosen_version: ContentVersionSummary | None = None
    versions: list[ContentVersionSummary]
    publish_records: list[PublishRecordSummary]
    latest_review_summary: str
    next_action: str


class MarkPublishedRequest(BaseModel):
    version_id: str | None = None
    platform: Literal["抖音", "小红书"] = "抖音"
    published_at: datetime
    views: int = 0
    likes: int = 0
    comments: int = 0
    favorites: int = 0
    shares: int = 0
    profile_visits: int = 0
    dm_count: int = 0
    inquiry_count: int = 0
    conversion_count: int = 0
    manual_notes: str | None = None


class ContentItemTimeline(BaseModel):
    item_id: str
    timeline: list[TimelineItem]


class NextPostRecommendationSummary(BaseModel):
    recommended_topic: str
    recommended_pillar: str
    recommended_content_type: str
    benchmark_reference_ids: list[str]
    why_this_now: str
    expected_goal: str
    recommended_hook_direction: str
    recommended_conversion_direction: str
    do_not_do: str
