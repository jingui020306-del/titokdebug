from __future__ import annotations

from app.decision.engines.account_stage_engine import account_stage_engine
from app.decision.engines.benchmark_selection_engine import benchmark_selection_engine
from app.decision.engines.gap_priority_engine import gap_priority_engine
from app.decision.engines.next_post_engine import next_post_engine
from app.decision.engines.review_decision_engine import review_decision_engine
from app.decision.engines.workflow_recommendation_engine import workflow_recommendation_engine
from app.decision.explain.llm_explainer import llm_explainer
from app.decision.snapshot.snapshot_builder import snapshot_builder
from app.schemas.decision import FrontstageDecisionBundle, WeeklyFocusSummary


class DecisionOrchestrator:
    """Unified authority for all frontstage/workspace key decisions.

    Runtime mode:
    - Engines remain rule-first in phase-1.
    - Retrieval/ranking/bandit/topic hooks are optional and fallback safely.
    - LLM is explanation-only and never acts as judge.
    """

    def build_bundle(self, user_id: str) -> FrontstageDecisionBundle:
        snapshot = snapshot_builder.build(user_id)
        account_stage = account_stage_engine.run(snapshot)
        gap_summary = gap_priority_engine.run(snapshot)
        learning_target = benchmark_selection_engine.run(snapshot, gap_summary.current_top_gap)
        next_post = next_post_engine.run(snapshot, gap_summary, learning_target)
        review_decision = review_decision_engine.run(snapshot)
        workflow = workflow_recommendation_engine.run(snapshot, account_stage, gap_summary, next_post, review_decision)

        weekly_focus = WeeklyFocusSummary(
            conclusion=f"本周先解决：{gap_summary.current_top_gap}",
            reason=gap_summary.why_it_is_top_priority,
            primary_actions=[gap_summary.what_to_fix_first, "发布 1 条承接型内容", "发布后补复盘"],
            risk_note="不要同时开启多个方向，否则难以判断动作是否有效。",
        )

        _ = llm_explainer.explain("workflow", workflow.model_dump())

        return FrontstageDecisionBundle(
            snapshot=snapshot,
            account_stage=account_stage,
            learning_target=learning_target,
            gap_summary=gap_summary,
            next_post=next_post,
            weekly_focus=weekly_focus,
            review_decision=review_decision,
            workflow_recommendation=workflow,
        )

    @staticmethod
    def build_card_views(bundle: FrontstageDecisionBundle) -> dict[str, dict[str, str]]:
        """Single source of truth for key card-ready decision fields."""
        return {
            "account_stage": {
                "conclusion": bundle.account_stage.stage,
                "reason": bundle.account_stage.reason,
                "evidence": "；".join(bundle.account_stage.evidence),
                "risk_note": "阶段未稳定前，不要频繁切方向。",
            },
            "learning_target": {
                "conclusion": f"{bundle.learning_target.selected_benchmark_account}（学{bundle.learning_target.learning_target_dimension}）",
                "reason": bundle.learning_target.why_this_account_now,
                "evidence": "；".join(bundle.learning_target.evidence),
                "risk_note": bundle.learning_target.what_not_to_copy,
            },
            "gap_summary": {
                "conclusion": bundle.gap_summary.current_top_gap,
                "reason": bundle.gap_summary.why_it_is_top_priority,
                "risk_note": bundle.gap_summary.what_happens_if_not_fixed,
                "first_action": bundle.gap_summary.what_to_fix_first,
            },
            "next_post": {
                "conclusion": bundle.next_post.recommended_topic,
                "reason": bundle.next_post.why_this_now,
                "risk_note": bundle.next_post.do_not_do,
                "goal": bundle.next_post.recommended_goal,
                "content_type": bundle.next_post.recommended_content_type,
                "hook_direction": bundle.next_post.recommended_hook_direction,
            },
            "weekly_focus": {
                "conclusion": bundle.weekly_focus.conclusion,
                "reason": bundle.weekly_focus.reason,
                "risk_note": bundle.weekly_focus.risk_note,
            },
            "next_step": {
                "conclusion": bundle.workflow_recommendation.best_next_action,
                "reason": bundle.workflow_recommendation.best_next_action_reason,
                "risk_note": "先闭环当前动作，再扩展新方向。",
            },
        }


decision_orchestrator = DecisionOrchestrator()
