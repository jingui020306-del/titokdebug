from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from app.decision.snapshot.schemas import UserGrowthSnapshot


class AccountStageSummary(BaseModel):
    stage: Literal["冷启动", "有方向但不稳", "正在贴近可承接咨询的结构", "已形成主打法"]
    confidence: int
    reason: str
    evidence: list[str]
    next_expected_milestone: str


class LearningTargetSummary(BaseModel):
    selected_benchmark_account: str
    learning_target_dimension: str
    why_this_account_now: str
    why_not_others: str
    what_to_learn: str
    what_not_to_copy: str
    confidence: int
    evidence: list[str]


class GapItem(BaseModel):
    dimension: str
    my_score: int
    benchmark_score: int
    gap_score: int
    urgency: Literal["now", "this_week", "later"]
    expected_impact: str
    effort_level: Literal["low", "medium", "high"]
    why_gap_exists: str
    first_fix_action: str


class GapSummary(BaseModel):
    gap_items: list[GapItem]
    current_top_gap: str
    why_it_is_top_priority: str
    what_happens_if_not_fixed: str
    what_to_fix_first: str


class NextPostRecommendation(BaseModel):
    recommended_topic: str
    recommended_pillar: str
    recommended_content_type: str
    recommended_goal: str
    recommended_hook_direction: str
    recommended_conversion_direction: str
    why_this_now: str
    benchmark_reference_ids: list[str]
    do_not_do: str
    alternative_options: list[str]


class WeeklyFocusSummary(BaseModel):
    conclusion: str
    reason: str
    primary_actions: list[str]
    risk_note: str


class ReviewDecisionSummary(BaseModel):
    bottleneck_stage: str
    problem_level: Literal["表达问题", "题型问题", "支柱问题", "切口问题"]
    recommended_action: Literal["放大", "继续测试", "改题型", "回内容执行", "回改造方案", "回我的账号", "停止此方向"]
    benchmark_learning_status: Literal["未开始学习", "正在模仿", "已初步贴近", "已形成自己的版本", "学错方向"]
    what_worked: list[str]
    what_failed: list[str]
    next_iteration_actions: list[str]
    should_scale_or_stop: str
    why: str


class WorkflowRecommendationSummary(BaseModel):
    current_workflow_stage: str
    best_next_action: str
    best_next_action_reason: str
    why_now: str
    blocking_issues: list[str]
    secondary_actions: list[str]


class FrontstageDecisionBundle(BaseModel):
    snapshot: UserGrowthSnapshot
    account_stage: AccountStageSummary
    learning_target: LearningTargetSummary
    gap_summary: GapSummary
    next_post: NextPostRecommendation
    weekly_focus: WeeklyFocusSummary
    review_decision: ReviewDecisionSummary
    workflow_recommendation: WorkflowRecommendationSummary
