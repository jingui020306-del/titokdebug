from __future__ import annotations

import json
from datetime import datetime

from app.core.db import get_conn
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


class SnapshotBuilder:
    def build(self, user_id: str) -> UserGrowthSnapshot:
        with get_conn() as conn:
            active_pos = conn.execute(
                "SELECT preview_text FROM positioning_versions WHERE user_id = ? AND is_active = 1 LIMIT 1", (user_id,)
            ).fetchone()
            frozen = conn.execute(
                "SELECT COUNT(1) as c FROM positioning_versions WHERE user_id = ? AND is_frozen = 1", (user_id,)
            ).fetchone()
            content_rows = conn.execute(
                "SELECT id, pillar, status FROM content_items WHERE user_id = ? ORDER BY updated_at DESC LIMIT 120", (user_id,)
            ).fetchall()
            version_rows = conn.execute(
                "SELECT v.id, v.content_item_id, v.version_label, v.created_at FROM content_versions v JOIN content_items c ON c.id = v.content_item_id WHERE c.user_id = ? ORDER BY v.created_at DESC LIMIT 120", (user_id,)
            ).fetchall()
            publish_rows = conn.execute(
                "SELECT p.id, p.content_item_id, p.published_at, p.metrics_json FROM publish_records p JOIN content_items c ON c.id = p.content_item_id WHERE c.user_id = ? ORDER BY p.published_at DESC LIMIT 120", (user_id,)
            ).fetchall()
            review_rows = conn.execute(
                "SELECT id, created_at, report_json FROM review_entries WHERE user_id = ? ORDER BY created_at DESC LIMIT 80", (user_id,)
            ).fetchall()
            pattern_rows = conn.execute(
                "SELECT id, pattern_type, label, summary, confidence, score, current_status, pattern_text FROM learned_patterns WHERE user_id = ? ORDER BY updated_at DESC LIMIT 120", (user_id,)
            ).fetchall()
            benchmark_rows = conn.execute(
                "SELECT id, account_name, account_tier, similarity_reason, learnability_reason, why_selected FROM benchmark_accounts WHERE user_id = ? ORDER BY updated_at DESC LIMIT 80", (user_id,)
            ).fetchall()
            sample_rows = conn.execute(
                "SELECT id, benchmark_account_id, title, content_type, pillar_guess, sample_heat_level FROM benchmark_content_samples WHERE benchmark_account_id IN (SELECT id FROM benchmark_accounts WHERE user_id = ?) ORDER BY updated_at DESC LIMIT 200",
                (user_id,),
            ).fetchall()
            todo_rows = conn.execute(
                "SELECT id, title, source_module, priority, status, action_type FROM todo_items WHERE user_id = ? ORDER BY created_at DESC LIMIT 80", (user_id,)
            ).fetchall()
            auth_row = conn.execute("SELECT status FROM douyin_authorizations WHERE user_id = ? LIMIT 1", (user_id,)).fetchone()

        records = [self._publish_row_to_snapshot(r) for r in publish_rows]
        reviews = [self._review_row_to_snapshot(r) for r in review_rows]
        content_items = [ContentItemSnapshot(id=r["id"], pillar=r["pillar"] or "", status=r["status"] or "planned") for r in content_rows]
        pillars = sorted({x.pillar for x in content_items if x.pillar})

        return UserGrowthSnapshot(
            user_id=user_id,
            active_positioning=ActivePositioningSnapshot(
                has_active=active_pos is not None,
                has_frozen=(frozen["c"] if frozen else 0) > 0,
                preview_text=active_pos["preview_text"] if active_pos else "",
            ),
            frozen_positioning=(frozen["c"] if frozen else 0) > 0,
            content_pillars=pillars,
            recent_content_items=content_items,
            recent_versions=[
                ContentVersionSnapshot(
                    id=r["id"],
                    content_item_id=r["content_item_id"],
                    version_label=r["version_label"] or "v1",
                    created_at=datetime.fromisoformat(r["created_at"]),
                )
                for r in version_rows
            ],
            publish_records=records,
            recent_reviews=reviews,
            learned_patterns=[
                LearnedPatternSnapshot(
                    id=r["id"],
                    pattern_type=r["pattern_type"] or "pillar",
                    label=r["label"] or r["pattern_text"] or "未命名模式",
                    summary=r["summary"] or r["pattern_text"] or "",
                    confidence=int(r["confidence"] if r["confidence"] is not None else (r["score"] or 50)),
                    current_status=r["current_status"] if r["current_status"] in {"candidate", "validated", "deprecated"} else "candidate",
                )
                for r in pattern_rows
            ],
            benchmark_accounts=[
                BenchmarkAccountSnapshot(
                    id=r["id"],
                    account_name=r["account_name"] or "",
                    account_tier=r["account_tier"] or "peer",
                    similarity_reason=r["similarity_reason"] or "",
                    learnability_reason=r["learnability_reason"] or "",
                    why_selected=r["why_selected"] or "",
                )
                for r in benchmark_rows
            ],
            benchmark_samples=[
                BenchmarkContentSampleSnapshot(
                    id=r["id"],
                    benchmark_account_id=r["benchmark_account_id"],
                    title=r["title"] or "",
                    content_type=r["content_type"] or "",
                    pillar_guess=r["pillar_guess"] or "",
                    sample_heat_level=r["sample_heat_level"] or "normal",
                )
                for r in sample_rows
            ],
            todo_items=[
                TodoItemSnapshot(
                    id=r["id"],
                    title=r["title"],
                    source_module=r["source_module"] or "workspace",
                    priority=r["priority"] or "medium",
                    status=r["status"] or "todo",
                    action_type=r["action_type"] or "rewrite_single_post",
                )
                for r in todo_rows
            ],
            account_goal="咨询",
            current_stage_hint=None,
            integration_status=IntegrationStatusSnapshot(
                douyin_connected=bool(auth_row and auth_row["status"] == "connected"),
                oauth_mode="official_oauth_placeholder",
            ),
        )

    @staticmethod
    def _publish_row_to_snapshot(row) -> PublishRecordSnapshot:
        metrics: dict[str, int] = {}
        raw = row["metrics_json"]
        if raw:
            try:
                metrics = json.loads(raw)
            except json.JSONDecodeError:
                metrics = {}
        return PublishRecordSnapshot(
            id=row["id"],
            content_item_id=row["content_item_id"],
            published_at=datetime.fromisoformat(row["published_at"]),
            views=int(metrics.get("views", 0)),
            likes=int(metrics.get("likes", 0)),
            comments=int(metrics.get("comments", 0)),
            favorites=int(metrics.get("favorites", 0)),
            shares=int(metrics.get("shares", 0)),
            profile_visits=int(metrics.get("profile_visits", 0)),
            dm_count=int(metrics.get("dm_count", 0)),
            inquiry_count=int(metrics.get("inquiry_count", 0)),
            conversion_count=int(metrics.get("conversion_count", 0)),
        )

    @staticmethod
    def _review_row_to_snapshot(row) -> ReviewEntrySnapshot:
        payload = {}
        raw = row["report_json"]
        if raw:
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {}
        return ReviewEntrySnapshot(
            id=row["id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            decision=str(payload.get("decision", "")),
            bottleneck_stage=str(payload.get("bottleneck_stage", "")),
            next_action=str(payload.get("next_action", "")),
        )


snapshot_builder = SnapshotBuilder()
