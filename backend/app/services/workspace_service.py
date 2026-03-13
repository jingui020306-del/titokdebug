from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.decision.engines.orchestrator import decision_orchestrator
from app.schemas.common import PatternItem, TimelineItem, TodoItem, WorkflowRecommendationSummary
from app.schemas.content_studio import NextPostRecommendationSummary
from app.schemas.workspace import WorkspaceSummary, WorkspaceTimeline


class WorkspaceService:
    def get_summary(self, user_id: str) -> WorkspaceSummary:
        bundle = decision_orchestrator.build_bundle(user_id)
        cards = decision_orchestrator.build_card_views(bundle)
        snapshot = bundle.snapshot

        validated = [x for x in snapshot.learned_patterns if x.current_status == "validated"][:5]
        stopped = [x for x in snapshot.learned_patterns if x.current_status == "deprecated"][:3]
        best = max(validated, key=lambda x: x.confidence, default=None)
        todos = [self._snapshot_todo_to_item(x, user_id) for x in snapshot.todo_items] or self._bootstrap_todos(user_id)

        pending_content_items = sum(1 for x in snapshot.recent_content_items if x.status in {"planned", "drafted", "adopted", "published"})
        unpublished_adopted_items = sum(1 for x in snapshot.recent_content_items if x.status == "adopted")
        unreviewed_published_items = max(0, len(snapshot.publish_records) - len(snapshot.recent_reviews))
        recent_7d_total_inquiries = sum(x.inquiry_count for x in snapshot.publish_records)
        recent_7d_consultation_content_count = len([x for x in snapshot.publish_records if x.inquiry_count > 0])

        item_pillar = {x.id: x.pillar for x in snapshot.recent_content_items}
        pillar_counts: dict[str, int] = {}
        for record in snapshot.publish_records:
            p = item_pillar.get(record.content_item_id, "咨询策略")
            pillar_counts[p] = pillar_counts.get(p, 0) + record.inquiry_count
        top_pillar = max(pillar_counts, key=pillar_counts.get) if pillar_counts else "咨询策略"

        return WorkspaceSummary(
            latest_positioning_summary=snapshot.active_positioning.preview_text or "先完成定位，避免方向漂移。",
            active_content_plan_summary="本周建议围绕 top gap 执行 3 条承接型内容。",
            latest_review_summary=bundle.review_decision.why,
            current_best_next_step=bundle.workflow_recommendation.best_next_action,
            current_workflow_stage=bundle.workflow_recommendation.current_workflow_stage,
            best_next_action=bundle.workflow_recommendation.best_next_action,
            best_next_action_reason=cards["next_step"]["reason"],
            pending_content_items=pending_content_items,
            unpublished_adopted_items=unpublished_adopted_items,
            unreviewed_published_items=unreviewed_published_items,
            recent_7d_consultation_content_count=recent_7d_consultation_content_count,
            recent_7d_total_inquiries=recent_7d_total_inquiries,
            top_consultation_pillar=top_pillar,
            active_frozen_positioning=snapshot.active_positioning.preview_text or "暂无冻结定位",
            benchmark_pool_size=len(snapshot.benchmark_accounts),
            strongest_accounts_to_learn=[bundle.learning_target.selected_benchmark_account],
            current_main_gap=bundle.gap_summary.current_top_gap,
            current_upgrade_focus=bundle.weekly_focus.conclusion,
            next_post_recommendation=NextPostRecommendationSummary(
                recommended_topic=bundle.next_post.recommended_topic,
                recommended_pillar=bundle.next_post.recommended_pillar,
                recommended_content_type=bundle.next_post.recommended_content_type,
                benchmark_reference_ids=bundle.next_post.benchmark_reference_ids,
                why_this_now=bundle.next_post.why_this_now,
                expected_goal=bundle.next_post.recommended_goal,
                recommended_hook_direction=bundle.next_post.recommended_hook_direction,
                recommended_conversion_direction=bundle.next_post.recommended_conversion_direction,
                do_not_do=bundle.next_post.do_not_do,
            ),
            why_next_post_now=bundle.next_post.why_this_now,
            current_learning_target=bundle.learning_target.learning_target_dimension,
            upgrade_plan_progress="改造进度：统一决策引擎已接管关键判断",
            todo_list=todos,
            learned_patterns_preview=[self._snapshot_pattern_to_item(x, user_id) for x in snapshot.learned_patterns[:5]],
            stopped_directions_preview=[self._snapshot_pattern_to_item(x, user_id) for x in stopped],
            best_to_scale_pattern=self._snapshot_pattern_to_item(best, user_id) if best else None,
            workflow_recommendation=WorkflowRecommendationSummary(
                current_workflow_stage=bundle.workflow_recommendation.current_workflow_stage,
                best_next_action=bundle.workflow_recommendation.best_next_action,
                best_next_action_reason=cards["next_step"]["reason"],
            ),
            decision_cards=cards,
        )

    def get_timeline(self, user_id: str) -> WorkspaceTimeline:
        with get_conn() as conn:
            arows = conn.execute("SELECT created_at, payload_json FROM audit_reports WHERE user_id = ? ORDER BY created_at DESC LIMIT 8", (user_id,)).fetchall()
            crows = conn.execute("SELECT created_at, payload_json FROM content_plan_jobs WHERE user_id = ? ORDER BY created_at DESC LIMIT 8", (user_id,)).fetchall()
            rrows = conn.execute("SELECT created_at, report_json FROM review_entries WHERE user_id = ? ORDER BY created_at DESC LIMIT 8", (user_id,)).fetchall()
            prows = conn.execute("SELECT * FROM learned_patterns WHERE user_id = ? ORDER BY updated_at DESC LIMIT 20", (user_id,)).fetchall()

        positioning_shifts = [
            TimelineItem(id=f"pos_{i}", event_type="positioning_shift", title="定位结论更新", summary=json.loads(x["payload_json"]).get("preview_text", "定位结论更新"), created_at=datetime.fromisoformat(x["created_at"]))
            for i, x in enumerate(arows)
        ]
        pillar_shifts = [
            TimelineItem(id=f"pillar_{i}", event_type="pillar_shift", title="内容支柱调整", summary=json.loads(x["payload_json"]).get("weekly_strategy_summary", "内容计划更新"), created_at=datetime.fromisoformat(x["created_at"]))
            for i, x in enumerate(crows)
        ]
        recent_reviews = [
            TimelineItem(id=f"review_{i}", event_type="review", title="复盘结论", summary=json.loads(x["report_json"]).get("performance_summary", "复盘更新"), created_at=datetime.fromisoformat(x["created_at"]))
            for i, x in enumerate(rrows)
        ]
        patterns = [self._pattern_row_to_item(x) for x in prows]
        validated = [x for x in patterns if x.current_status == "validated"]
        stopped = [x for x in patterns if x.current_status == "deprecated"]
        timeline_items = sorted([*positioning_shifts, *pillar_shifts, *recent_reviews], key=lambda x: x.created_at, reverse=True)
        return WorkspaceTimeline(
            positioning_shifts=positioning_shifts,
            pillar_shifts=pillar_shifts,
            recent_reviews=recent_reviews,
            validated_patterns=validated,
            stopped_directions=stopped,
            timeline_items=timeline_items,
        )

    def update_todo_status(self, user_id: str, todo_id: str, status: str) -> bool:
        if status not in {"todo", "in_progress", "paused", "done"}:
            return False
        now = datetime.now(timezone.utc).isoformat()
        with get_conn() as conn:
            cur = conn.execute("UPDATE todo_items SET status = ?, updated_at = ? WHERE id = ? AND user_id = ?", (status, now, todo_id, user_id))
        return cur.rowcount > 0

    def _bootstrap_todos(self, user_id: str) -> list[TodoItem]:
        defaults = [
            ("修改主页表达", "positioning", "rewrite_profile"),
            ("生成本周计划", "content_studio", "generate_weekly_plan"),
            ("改某条内容", "content_studio", "rewrite_single_post"),
            ("回填复盘", "review_lab", "fill_review"),
            ("放大某支柱", "review_lab", "scale_pillar"),
            ("停止某方向", "review_lab", "stop_direction"),
        ]
        now = datetime.now(timezone.utc)
        items: list[TodoItem] = []
        with get_conn() as conn:
            for title, mod, action in defaults:
                todo_id = f"td_{uuid.uuid4().hex[:10]}"
                conn.execute(
                    "INSERT INTO todo_items (id, user_id, title, source_module, source_report_id, priority, status, action_type, suggested_due_label, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (todo_id, user_id, title, mod, None, "medium", "todo", action, "本周", now.isoformat(), now.isoformat()),
                )
                items.append(TodoItem(id=todo_id, user_id=user_id, title=title, source_module=mod, source_report_id=None, priority="medium", status="todo", action_type=action, suggested_due_label="本周", created_at=now, updated_at=now))
        return items

    @staticmethod
    def _snapshot_todo_to_item(row, user_id: str) -> TodoItem:
        now = datetime.now(timezone.utc)
        return TodoItem(
            id=row.id,
            user_id=user_id,
            title=row.title,
            source_module=row.source_module,
            source_report_id=None,
            priority=row.priority,
            status=row.status,
            action_type=row.action_type,
            suggested_due_label="本周",
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _snapshot_pattern_to_item(row, user_id: str) -> PatternItem:
        now = datetime.now(timezone.utc)
        return PatternItem(
            id=row.id,
            user_id=user_id,
            pattern_type=row.pattern_type if row.pattern_type in {"title_style", "hook_style", "pillar", "profile_expression", "conversion_cta", "risk_direction"} else "pillar",
            label=row.label,
            summary=row.summary,
            evidence_source="decision_snapshot",
            confidence=int(row.confidence),
            current_status=row.current_status,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _todo_row_to_item(row) -> TodoItem:
        return TodoItem(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            source_module=row["source_module"],
            source_report_id=row["source_report_id"],
            priority=row["priority"],
            status=row["status"],
            action_type=row["action_type"],
            suggested_due_label=row["suggested_due_label"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    @staticmethod
    def _pattern_row_to_item(row) -> PatternItem:
        return PatternItem(
            id=row["id"],
            user_id=row["user_id"],
            pattern_type=row["pattern_type"],
            label=row["label"],
            summary=row["summary"],
            evidence_source=row["evidence_source"],
            confidence=int(row["confidence"]),
            current_status=row["current_status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )


workspace_service = WorkspaceService()
