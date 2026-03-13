from __future__ import annotations

from app.decision.engines.orchestrator import decision_orchestrator
from app.services.workspace_service import workspace_service


class FrontstageService:
    def home_summary(self, user_id: str) -> dict:
        bundle = decision_orchestrator.build_bundle(user_id)
        cards = decision_orchestrator.build_card_views(bundle)
        return {
            "account_stage": cards["account_stage"]["conclusion"],
            "learning_target": cards["learning_target"]["conclusion"],
            "main_gap": cards["gap_summary"]["conclusion"],
            "next_post": bundle.next_post.model_dump(mode="json"),
            "weekly_focus": cards["weekly_focus"]["conclusion"],
            "best_next_action": cards["next_step"]["conclusion"],
            "best_next_action_reason": cards["next_step"]["reason"],
            "decision_cards": cards,
            "douyin_status": "开发模式（未接真实账号）",
            "last_review_time": "近期",
        }

    def my_account_summary(self, user_id: str) -> dict:
        bundle = decision_orchestrator.build_bundle(user_id)
        snap = bundle.snapshot
        return {
            "current_positioning_summary": snap.active_positioning.preview_text or "先完成定位，建立账号基线",
            "account_stage": bundle.account_stage.stage,
            "active_positioning": {"preview_text": snap.active_positioning.preview_text} if snap.active_positioning.preview_text else None,
            "frozen": snap.frozen_positioning,
            "three_pillars": snap.content_pillars[:3] or ["咨询策略", "案例拆解", "表达优化"],
            "off_limits": ["泛鸡汤", "无承接纯观点"],
            "evidence_chain": bundle.account_stage.evidence,
            "next_actions": ["去值得学的账号", "去改造方案", "去内容执行"],
        }

    def learn_from_summary(self, user_id: str) -> dict:
        bundle = decision_orchestrator.build_bundle(user_id)
        snap = bundle.snapshot
        return {
            "benchmark_pool_size": len(snap.benchmark_accounts),
            "top_accounts": [
                {
                    "id": x.id,
                    "account_name": x.account_name,
                    "learnability_reason": x.learnability_reason,
                    "similarity_reason": x.similarity_reason,
                }
                for x in snap.benchmark_accounts[:3]
            ],
            "entry_actions": ["我自己添加 5 个账号", "帮我找像我且值得学的账号"],
            "recent_added": [x.account_name for x in snap.benchmark_accounts[:5]],
            "priority_samples": f"优先学习：{bundle.learning_target.what_to_learn}",
        }

    def upgrade_plan_summary(self, user_id: str) -> dict:
        bundle = decision_orchestrator.build_bundle(user_id)
        return {
            "current_main_gap": bundle.gap_summary.current_top_gap,
            "top3_changes": [bundle.gap_summary.what_to_fix_first, *bundle.weekly_focus.primary_actions[:2]],
            "profile_upgrade": ["主页 headline 改成服务对象+结果", "简介加入咨询承接路径"],
            "content_structure_upgrade": [f"优先补齐 {bundle.gap_summary.current_top_gap}", "减少泛流量无承接内容"],
            "content_type_upgrade": [bundle.next_post.recommended_content_type, "问题拆解 + 案例反转"],
            "next_7_posts": [bundle.next_post.recommended_topic, *bundle.next_post.alternative_options],
        }

    def execute_summary(self, user_id: str) -> dict:
        bundle = decision_orchestrator.build_bundle(user_id)
        ws = workspace_service.get_summary(user_id)
        return {
            "weekly_plan_summary": ws.active_content_plan_summary,
            "next_post_recommendation": bundle.next_post.model_dump(mode="json"),
            "pending_publish": ws.unpublished_adopted_items,
            "recent_rewrites": "按 top gap 生成改单条，优先执行高咨询承接题型。",
            "benchmark_learning_preview": [bundle.learning_target.selected_benchmark_account],
            "actions": ["去执行这一条", "去标记已发布", "去补复盘"],
        }

    def review_summary(self, user_id: str) -> dict:
        bundle = decision_orchestrator.build_bundle(user_id)
        return {
            "latest_review_summary": bundle.review_decision.why,
            "best_pillar": bundle.next_post.recommended_pillar,
            "best_content_type": bundle.next_post.recommended_content_type,
            "stopped_directions": bundle.review_decision.what_failed,
            "latest_better_or_worse": bundle.review_decision.should_scale_or_stop,
            "actions": ["去完整复盘", "去模式资产", "去改造方案"],
        }


frontstage_service = FrontstageService()
