from __future__ import annotations

from datetime import datetime, timezone
import unittest

from app.decision.engines.account_stage_engine import account_stage_engine
from app.decision.engines.benchmark_selection_engine import benchmark_selection_engine
from app.decision.engines.gap_priority_engine import gap_priority_engine
from app.decision.engines.next_post_engine import next_post_engine
from app.decision.engines.orchestrator import DecisionOrchestrator
from app.decision.engines.workflow_recommendation_engine import workflow_recommendation_engine
from app.core.db import init_db
from app.services.frontstage_service import frontstage_service
from app.services.workspace_service import workspace_service
from app.decision.snapshot.schemas import (
    ActivePositioningSnapshot,
    BenchmarkAccountSnapshot,
    BenchmarkContentSampleSnapshot,
    ContentItemSnapshot,
    ContentVersionSnapshot,
    IntegrationStatusSnapshot,
    LearnedPatternSnapshot,
    PublishRecordSnapshot,
    ReviewEntrySnapshot,
    TodoItemSnapshot,
    UserGrowthSnapshot,
)
from app.schemas.decision import ReviewDecisionSummary


def make_snapshot(
    *,
    has_active: bool = True,
    has_frozen: bool = True,
    benchmark_count: int = 3,
    inquiry: int = 0,
    conversion: int = 0,
    include_review: bool = True,
    include_published: bool = True,
) -> UserGrowthSnapshot:
    now = datetime.now(timezone.utc)
    benchmarks = [
        BenchmarkAccountSnapshot(
            id=f"b{i}",
            account_name=f"bench-{i}",
            account_tier="mid" if i == 0 else "peer",
            similarity_reason="同赛道咨询内容结构相似",
            learnability_reason="评论区承接动作稳定",
            why_selected="可复用承接结构",
        )
        for i in range(benchmark_count)
    ]

    publish = [
        PublishRecordSnapshot(
            id="p1",
            content_item_id="c1",
            published_at=now,
            views=1200,
            likes=100,
            comments=15,
            favorites=6,
            shares=4,
            profile_visits=25,
            dm_count=max(0, inquiry - 1),
            inquiry_count=inquiry,
            conversion_count=conversion,
        )
    ] if include_published else []

    reviews = [
        ReviewEntrySnapshot(
            id="r1",
            created_at=now,
            decision="继续测试",
            bottleneck_stage="承接",
            next_action="继续测试",
        )
    ] if include_review else []

    return UserGrowthSnapshot(
        user_id="u1",
        active_positioning=ActivePositioningSnapshot(has_active=has_active, has_frozen=has_frozen, preview_text="定位" if has_active else ""),
        frozen_positioning=has_frozen,
        content_pillars=["咨询策略", "案例拆解"],
        recent_content_items=[ContentItemSnapshot(id="c1", pillar="咨询策略", status="published")],
        recent_versions=[ContentVersionSnapshot(id="v1", content_item_id="c1", version_label="v1", created_at=now)],
        publish_records=publish,
        recent_reviews=reviews,
        learned_patterns=[LearnedPatternSnapshot(id="lp1", pattern_type="hook_style", label="问题开场", summary="先问后给", confidence=80, current_status="validated")],
        benchmark_accounts=benchmarks,
        benchmark_samples=[BenchmarkContentSampleSnapshot(id="s1", benchmark_account_id="b0", title="样本", content_type="案例型", pillar_guess="咨询策略", sample_heat_level="strong")],
        todo_items=[TodoItemSnapshot(id="t1", title="执行下一条", source_module="workspace", priority="high", status="todo", action_type="rewrite_single_post")],
        account_goal="咨询",
        integration_status=IntegrationStatusSnapshot(douyin_connected=True, oauth_mode="official_oauth_placeholder"),
    )


class DecisionEngineTests(unittest.TestCase):
    def test_account_stage_engine(self):
        snap = make_snapshot(has_active=False, has_frozen=False, benchmark_count=0, include_published=False)
        result = account_stage_engine.run(snap)
        self.assertIn(result.stage, {"冷启动", "有方向但不稳"})

    def test_benchmark_selection_engine_fallback(self):
        snap = make_snapshot(benchmark_count=0)
        gap = gap_priority_engine.run(snap)
        result = benchmark_selection_engine.run(snap, gap.current_top_gap)
        self.assertEqual(result.selected_benchmark_account, "暂无")

    def test_gap_priority_engine_top_gap(self):
        snap = make_snapshot(inquiry=0)
        result = gap_priority_engine.run(snap)
        self.assertTrue(result.current_top_gap)
        self.assertGreaterEqual(len(result.gap_items), 8)

    def test_next_post_recommendation_stable(self):
        snap = make_snapshot(inquiry=1)
        gap = gap_priority_engine.run(snap)
        learn = benchmark_selection_engine.run(snap, gap.current_top_gap)
        nxt = next_post_engine.run(snap, gap, learn)
        self.assertTrue(nxt.recommended_topic)
        self.assertTrue(nxt.alternative_options)

    def test_workflow_without_active_positioning(self):
        snap = make_snapshot(has_active=False)
        stage = account_stage_engine.run(snap)
        gap = gap_priority_engine.run(snap)
        learn = benchmark_selection_engine.run(snap, gap.current_top_gap)
        nxt = next_post_engine.run(snap, gap, learn)
        rev = ReviewDecisionSummary(
            bottleneck_stage="",
            problem_level="切口问题",
            recommended_action="继续测试",
            benchmark_learning_status="未开始学习",
            what_worked=[],
            what_failed=[],
            next_iteration_actions=[],
            should_scale_or_stop="继续测试",
            why="",
        )
        wf = workflow_recommendation_engine.run(snap, stage, gap, nxt, rev)
        self.assertIn("定位", wf.best_next_action)

    def test_workflow_with_published_unreviewed_points_to_review(self):
        snap = make_snapshot(include_review=False, include_published=True)
        stage = account_stage_engine.run(snap)
        gap = gap_priority_engine.run(snap)
        learn = benchmark_selection_engine.run(snap, gap.current_top_gap)
        nxt = next_post_engine.run(snap, gap, learn)
        rev = ReviewDecisionSummary(
            bottleneck_stage="",
            problem_level="切口问题",
            recommended_action="继续测试",
            benchmark_learning_status="未开始学习",
            what_worked=[],
            what_failed=[],
            next_iteration_actions=[],
            should_scale_or_stop="继续测试",
            why="",
        )
        wf = workflow_recommendation_engine.run(snap, stage, gap, nxt, rev)
        self.assertIn("复盘", wf.best_next_action)

    def test_orchestrator_build_bundle(self):
        orch = DecisionOrchestrator()
        init_db()
        # Only validate structure on unknown user fallback paths.
        bundle = orch.build_bundle("dev-user")
        self.assertTrue(bundle.account_stage.stage)
        self.assertTrue(bundle.workflow_recommendation.best_next_action)

    def test_frontstage_and_workspace_share_same_decision_source(self):
        init_db()
        home = frontstage_service.home_summary("dev-user")
        ws = workspace_service.get_summary("dev-user")
        self.assertEqual(home["account_stage"], ws.decision_cards["account_stage"]["conclusion"])
        self.assertEqual(home["main_gap"], ws.current_main_gap)
        self.assertEqual(home["best_next_action"], ws.best_next_action)
        self.assertEqual(home["decision_cards"]["next_post"]["conclusion"], ws.decision_cards["next_post"]["conclusion"])

    def test_frontstage_summary_works_without_optional_algo_deps(self):
        init_db()
        # Using default environment (optional deps may be absent), summary should still be produced.
        home = frontstage_service.home_summary("dev-user")
        self.assertTrue(home["decision_cards"]["learning_target"]["conclusion"])
        self.assertTrue(home["next_post"]["recommended_topic"])


if __name__ == "__main__":
    unittest.main()
