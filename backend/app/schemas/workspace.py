from __future__ import annotations

from app.schemas.common import PatternItem, TimelineItem, TodoItem, WorkflowRecommendationSummary
from app.schemas.content_studio import NextPostRecommendationSummary
from pydantic import BaseModel


class WorkspaceSummary(BaseModel):
    latest_positioning_summary: str
    active_content_plan_summary: str
    latest_review_summary: str
    current_best_next_step: str
    current_workflow_stage: str
    best_next_action: str
    best_next_action_reason: str
    pending_content_items: int
    unpublished_adopted_items: int
    unreviewed_published_items: int
    recent_7d_consultation_content_count: int
    recent_7d_total_inquiries: int
    top_consultation_pillar: str
    active_frozen_positioning: str
    benchmark_pool_size: int
    strongest_accounts_to_learn: list[str]
    current_main_gap: str
    current_upgrade_focus: str
    next_post_recommendation: NextPostRecommendationSummary
    why_next_post_now: str
    current_learning_target: str
    upgrade_plan_progress: str
    todo_list: list[TodoItem]
    learned_patterns_preview: list[PatternItem]
    stopped_directions_preview: list[PatternItem]
    best_to_scale_pattern: PatternItem | None
    workflow_recommendation: WorkflowRecommendationSummary
    decision_cards: dict[str, dict[str, str]] | None = None


class WorkspaceTimeline(BaseModel):
    positioning_shifts: list[TimelineItem]
    pillar_shifts: list[TimelineItem]
    recent_reviews: list[TimelineItem]
    validated_patterns: list[PatternItem]
    stopped_directions: list[PatternItem]
    timeline_items: list[TimelineItem]
