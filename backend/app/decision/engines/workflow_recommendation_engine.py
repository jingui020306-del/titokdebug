from __future__ import annotations

"""Workflow recommendation engine (rule state machine, phase-1)."""

from app.decision.snapshot.feature_store import SnapshotFeatureStore
from app.decision.snapshot.schemas import UserGrowthSnapshot
from app.schemas.decision import AccountStageSummary, GapSummary, NextPostRecommendation, ReviewDecisionSummary, WorkflowRecommendationSummary


class WorkflowRecommendationEngine:
    def run(
        self,
        snapshot: UserGrowthSnapshot,
        account_stage: AccountStageSummary,
        gap_summary: GapSummary,
        next_post: NextPostRecommendation,
        review_decision: ReviewDecisionSummary,
    ) -> WorkflowRecommendationSummary:
        fs = SnapshotFeatureStore(snapshot)

        if not snapshot.integration_status.douyin_connected:
            return WorkflowRecommendationSummary(
                current_workflow_stage="连接前准备",
                best_next_action="先连接抖音官方 OAuth",
                best_next_action_reason="未连接账号会导致真实反馈数据缺失。",
                why_now="先连接再执行可避免决策误差。",
                blocking_issues=["账号未连接"],
                secondary_actions=["可先使用演示数据熟悉流程"],
            )

        if not snapshot.active_positioning.has_active:
            return WorkflowRecommendationSummary(
                current_workflow_stage="定位未完成",
                best_next_action="先完成我的账号定位",
                best_next_action_reason="没有定位会导致内容动作分散。",
                why_now="先补定位是后续动作前提。",
                blocking_issues=["active positioning 缺失"],
                secondary_actions=["可先建立对标池候选"],
            )

        if len(snapshot.benchmark_accounts) == 0:
            return WorkflowRecommendationSummary(
                current_workflow_stage="对标池未建立",
                best_next_action="先建立 3-5 个值得学账号",
                best_next_action_reason="无学习对象会让改造方向失真。",
                why_now="先明确学习参照，再执行内容动作。",
                blocking_issues=["benchmark pool 为空"],
                secondary_actions=["先手动添加 3 个同赛道账号"],
            )

        unreviewed = fs.unreviewed_published_count
        if unreviewed > 0:
            return WorkflowRecommendationSummary(
                current_workflow_stage=account_stage.stage,
                best_next_action="先补复盘",
                best_next_action_reason="存在已发布未复盘内容，先闭环再扩量。",
                why_now="复盘缺失会放大错误动作。",
                blocking_issues=[f"published 未复盘={unreviewed}"],
                secondary_actions=["再执行下一条推荐内容"],
            )

        if any(x.status == "adopted" for x in snapshot.recent_content_items):
            return WorkflowRecommendationSummary(
                current_workflow_stage=account_stage.stage,
                best_next_action="先发布已采用内容",
                best_next_action_reason="已有高置信内容，先发布拿反馈。",
                why_now="发布是最快减少不确定性的动作。",
                blocking_issues=["存在 adopted 未发布内容"],
                secondary_actions=["发布后 24-48 小时补复盘"],
            )

        if review_decision.recommended_action in {"回改造方案", "回我的账号"}:
            return WorkflowRecommendationSummary(
                current_workflow_stage=account_stage.stage,
                best_next_action=review_decision.recommended_action,
                best_next_action_reason="最近复盘显示当前打法偏离目标。",
                why_now="先纠偏再执行可避免继续损耗。",
                blocking_issues=["复盘建议回退"],
                secondary_actions=["重看 top gap", "重选学习对象"],
            )

        return WorkflowRecommendationSummary(
            current_workflow_stage=account_stage.stage,
            best_next_action=f"先执行下一条：{next_post.recommended_topic}",
            best_next_action_reason=f"当前 top gap={gap_summary.current_top_gap}，该动作收益最高。",
            why_now="先完成最小验证闭环，再决定是否放大。",
            blocking_issues=[],
            secondary_actions=["完成后立即补复盘"],
        )


workflow_recommendation_engine = WorkflowRecommendationEngine()
