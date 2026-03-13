from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.schemas.common import ContentItemSummary, ContentVersionSummary, PublishRecordSummary, TimelineItem
from app.schemas.content_studio import ContentHistoryItem, ContentItemDetail, ContentItemTimeline, MarkPublishedRequest, NextPostRecommendationSummary, WeeklyPlanReport, WeeklyPlanRequest


class ContentStudioService:
    def create_weekly_plan(self, user_id: str, payload: WeeklyPlanRequest) -> str:
        plan_id = f"cp_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc)
        calendar: list[dict[str, str | bool]] = []
        total = max(1, min(payload.posts_per_week, 7))
        for i in range(total):
            pillar = payload.content_pillars[i % max(1, len(payload.content_pillars))] if payload.content_pillars else "默认支柱"
            title_direction = f"{pillar}：本周第{i + 1}条选题方向"
            calendar.append(
                {
                    "day": f"day{i+1}",
                    "title_direction": title_direction,
                    "content_purpose": payload.weekly_goal,
                    "pillar": pillar,
                    "for_live_warmup": bool(payload.has_live and i in (2, 4)),
                    "for_consultation": bool(i in (1, total - 1)),
                }
            )
        report = WeeklyPlanReport(
            plan_id=plan_id,
            created_at=now,
            report_title="内容台周计划",
            preview_text="本周先稳住主线节奏，再做咨询承接内容。",
            recommended_next_module="content_studio",
            weekly_strategy_summary="围绕定位台结论做一周稳定输出，目标是提升咨询线索密度。",
            content_calendar=calendar,
            pillar_distribution=[{"pillar": p, "count": sum(1 for x in calendar if x["pillar"] == p)} for p in set(x["pillar"] for x in calendar)],
            live_topic_suggestions=["直播：本周高频问题答疑", "直播：案例复盘与动作清单"],
            consultation_conversion_posts=["案例前后对比", "咨询流程拆解"],
            high_risk_topics_to_avoid=["绝对化承诺", "过度收益暗示"],
        )
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO content_plan_jobs (id, user_id, status, payload_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (plan_id, user_id, "ready", json.dumps(report.model_dump(mode="json"), ensure_ascii=False), now.isoformat(), now.isoformat()),
            )
            for row in calendar:
                item_id = f"ci_{uuid.uuid4().hex[:10]}"
                title = str(row["title_direction"])
                conn.execute(
                    """
                    INSERT INTO content_items
                    (id, user_id, title, title_or_working_title, pillar, content_goal, source_plan_id, source_positioning_id, status, chosen_version_id, latest_publish_record_id, latest_review_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item_id,
                        user_id,
                        title,
                        title,
                        str(row["pillar"]),
                        str(row["content_purpose"]),
                        plan_id,
                        None,
                        "planned",
                        None,
                        None,
                        None,
                        now.isoformat(),
                        now.isoformat(),
                    ),
                )
        return plan_id

    def get_weekly_plan(self, user_id: str, plan_id: str) -> WeeklyPlanReport | None:
        with get_conn() as conn:
            row = conn.execute("SELECT payload_json FROM content_plan_jobs WHERE id = ? AND user_id = ?", (plan_id, user_id)).fetchone()
        if not row:
            return None
        return WeeklyPlanReport(**json.loads(row["payload_json"]))

    def create_or_update_version_from_rewrite(
        self,
        user_id: str,
        *,
        rewrite_id: str,
        content_item_id: str | None,
        title: str,
        pillar: str,
        cover_text: str,
        hook: str,
        body_script: str,
        closing_cta: str,
        comment_guide: str,
        risk_notes: str,
    ) -> str:
        now = datetime.now(timezone.utc)
        with get_conn() as conn:
            item_id = content_item_id
            if not item_id:
                item_id = f"ci_{uuid.uuid4().hex[:10]}"
                conn.execute(
                    """
                    INSERT INTO content_items
                    (id, user_id, title, title_or_working_title, pillar, content_goal, source_plan_id, source_positioning_id, status, chosen_version_id, latest_publish_record_id, latest_review_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (item_id, user_id, title, title, pillar, "转咨询", None, None, "drafted", None, None, None, now.isoformat(), now.isoformat()),
                )
            count_row = conn.execute("SELECT COUNT(1) as c FROM content_versions WHERE content_item_id = ?", (item_id,)).fetchone()
            version_no = int(count_row["c"]) + 1 if count_row else 1
            version_id = f"cv_{uuid.uuid4().hex[:10]}"
            payload = {
                "title": title,
                "cover_text": cover_text,
                "hook": hook,
                "body_script": body_script,
                "closing_cta": closing_cta,
                "comment_guide": comment_guide,
                "risk_notes": risk_notes,
            }
            conn.execute(
                """
                INSERT INTO content_versions
                (id, content_item_id, rewrite_job_id, version_label, payload_json, title, cover_text, hook, body_script, closing_cta, comment_guide, risk_notes, is_adopted, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version_id,
                    item_id,
                    rewrite_id,
                    f"V{version_no}",
                    json.dumps(payload, ensure_ascii=False),
                    title,
                    cover_text,
                    hook,
                    body_script,
                    closing_cta,
                    comment_guide,
                    risk_notes,
                    1,
                    now.isoformat(),
                    now.isoformat(),
                ),
            )
            conn.execute("UPDATE content_versions SET is_adopted = 0, updated_at = ? WHERE content_item_id = ? AND id != ?", (now.isoformat(), item_id, version_id))
            conn.execute(
                "UPDATE content_items SET chosen_version_id = ?, status = 'adopted', updated_at = ? WHERE id = ? AND user_id = ?",
                (version_id, now.isoformat(), item_id, user_id),
            )
        return version_id

    def mark_published(self, user_id: str, item_id: str, payload: MarkPublishedRequest) -> str:
        now = datetime.now(timezone.utc)
        record_id = f"pb_{uuid.uuid4().hex[:10]}"
        with get_conn() as conn:
            row = conn.execute("SELECT chosen_version_id FROM content_items WHERE id = ? AND user_id = ?", (item_id, user_id)).fetchone()
            if not row:
                raise KeyError(item_id)
            version_id = payload.version_id or row["chosen_version_id"]
            conn.execute(
                """
                INSERT INTO publish_records
                (id, content_item_id, version_id, platform, published_at, views, likes, comments, favorites, shares, profile_visits, dm_count, inquiry_count, conversion_count, manual_notes, created_at, updated_at, metrics_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    item_id,
                    version_id,
                    payload.platform,
                    payload.published_at.isoformat(),
                    payload.views,
                    payload.likes,
                    payload.comments,
                    payload.favorites,
                    payload.shares,
                    payload.profile_visits,
                    payload.dm_count,
                    payload.inquiry_count,
                    payload.conversion_count,
                    payload.manual_notes,
                    now.isoformat(),
                    now.isoformat(),
                    json.dumps(payload.model_dump(mode="json"), ensure_ascii=False),
                ),
            )
            conn.execute(
                "UPDATE content_items SET status = 'published', latest_publish_record_id = ?, updated_at = ? WHERE id = ? AND user_id = ?",
                (record_id, now.isoformat(), item_id, user_id),
            )
        return record_id

    def archive_item(self, user_id: str, item_id: str) -> bool:
        with get_conn() as conn:
            cur = conn.execute("UPDATE content_items SET status = 'archived', updated_at = ? WHERE id = ? AND user_id = ?", (datetime.now(timezone.utc).isoformat(), item_id, user_id))
        return cur.rowcount > 0

    def list_items(self, user_id: str) -> list[ContentItemSummary]:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM content_items WHERE user_id = ? ORDER BY updated_at DESC LIMIT 100",
                (user_id,),
            ).fetchall()
        return [self._row_to_item_summary(r) for r in rows]

    def get_item_detail(self, user_id: str, item_id: str) -> ContentItemDetail | None:
        with get_conn() as conn:
            item = conn.execute("SELECT * FROM content_items WHERE id = ? AND user_id = ?", (item_id, user_id)).fetchone()
            if not item:
                return None
            vrows = conn.execute("SELECT * FROM content_versions WHERE content_item_id = ? ORDER BY created_at DESC", (item_id,)).fetchall()
            prows = conn.execute("SELECT * FROM publish_records WHERE content_item_id = ? ORDER BY published_at DESC", (item_id,)).fetchall()
            review = conn.execute("SELECT report_json FROM review_entries WHERE content_item_id = ? AND user_id = ? ORDER BY created_at DESC LIMIT 1", (item_id, user_id)).fetchone()

        versions = [self._row_to_version_summary(r) for r in vrows]
        chosen = next((v for v in versions if v.id == item["chosen_version_id"]), None)
        publishes = [self._row_to_publish_summary(r) for r in prows]
        latest_review_summary = "暂无复盘"
        next_action = "先完成发布，再进入复盘"
        if review:
            payload = json.loads(review["report_json"])
            latest_review_summary = payload.get("preview_text", "已有复盘结论")
            next_action = (payload.get("next_iteration_actions") or ["继续执行下一步"])[0]
        return ContentItemDetail(
            item=self._row_to_item_summary(item),
            chosen_version=chosen,
            versions=versions,
            publish_records=publishes,
            latest_review_summary=latest_review_summary,
            next_action=next_action,
        )

    def list_versions(self, user_id: str, item_id: str) -> list[ContentVersionSummary]:
        with get_conn() as conn:
            item = conn.execute("SELECT id FROM content_items WHERE id = ? AND user_id = ?", (item_id, user_id)).fetchone()
            if not item:
                return []
            rows = conn.execute("SELECT * FROM content_versions WHERE content_item_id = ? ORDER BY created_at DESC", (item_id,)).fetchall()
        return [self._row_to_version_summary(r) for r in rows]

    def get_item_timeline(self, user_id: str, item_id: str) -> ContentItemTimeline:
        with get_conn() as conn:
            item = conn.execute("SELECT * FROM content_items WHERE id = ? AND user_id = ?", (item_id, user_id)).fetchone()
            if not item:
                return ContentItemTimeline(item_id=item_id, timeline=[])
            vrows = conn.execute("SELECT id, version_label, created_at FROM content_versions WHERE content_item_id = ? ORDER BY created_at DESC", (item_id,)).fetchall()
            prows = conn.execute("SELECT id, published_at, platform FROM publish_records WHERE content_item_id = ? ORDER BY published_at DESC", (item_id,)).fetchall()
            rrows = conn.execute("SELECT id, created_at FROM review_entries WHERE content_item_id = ? AND user_id = ? ORDER BY created_at DESC", (item_id, user_id)).fetchall()

        timeline: list[TimelineItem] = [
            TimelineItem(id=item["id"], event_type="item", title="创建内容对象", summary=item["title_or_working_title"] or item["title"], created_at=datetime.fromisoformat(item["created_at"]))
        ]
        timeline.extend(
            TimelineItem(id=r["id"], event_type="version", title=f"生成版本 {r['version_label']}", summary="已进入版本池", created_at=datetime.fromisoformat(r["created_at"]))
            for r in vrows
        )
        timeline.extend(
            TimelineItem(id=r["id"], event_type="publish", title=f"发布到{r['platform']}", summary="已记录发布结果", created_at=datetime.fromisoformat(r["published_at"]))
            for r in prows
        )
        timeline.extend(
            TimelineItem(id=r["id"], event_type="review", title="完成复盘", summary="已更新下一轮动作", created_at=datetime.fromisoformat(r["created_at"]))
            for r in rrows
        )
        timeline.sort(key=lambda x: x.created_at, reverse=True)
        return ContentItemTimeline(item_id=item_id, timeline=timeline)

    def get_history(self, user_id: str) -> list[ContentHistoryItem]:
        items: list[ContentHistoryItem] = []
        with get_conn() as conn:
            rows = conn.execute("SELECT id, status, created_at, payload_json FROM content_plan_jobs WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
            for row in rows:
                payload = json.loads(row["payload_json"]) if row["payload_json"] else {}
                items.append(ContentHistoryItem(id=row["id"], kind="weekly_plan", created_at=datetime.fromisoformat(row["created_at"]), title=payload.get("report_title", "周计划"), status=row["status"]))
            rrows = conn.execute("SELECT id, status, created_at FROM rewrite_engine_jobs WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
            for row in rrows:
                items.append(ContentHistoryItem(id=row["id"], kind="rewrite", created_at=datetime.fromisoformat(row["created_at"]), title="改单条", status=row["status"]))
        return sorted(items, key=lambda x: x.created_at, reverse=True)

    @staticmethod
    def _row_to_item_summary(row) -> ContentItemSummary:
        return ContentItemSummary(
            id=row["id"],
            title_or_working_title=row["title_or_working_title"] or row["title"],
            pillar=row["pillar"],
            content_goal=row["content_goal"] or "转咨询",
            status=row["status"],
            chosen_version_id=row["chosen_version_id"],
            latest_publish_record_id=row["latest_publish_record_id"],
            latest_review_id=row["latest_review_id"],
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    @staticmethod
    def _row_to_version_summary(row) -> ContentVersionSummary:
        return ContentVersionSummary(
            id=row["id"],
            content_item_id=row["content_item_id"],
            version_label=row["version_label"],
            title=row["title"] or row["version_label"],
            hook=row["hook"] or "",
            is_adopted=bool(row["is_adopted"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    @staticmethod
    def _row_to_publish_summary(row) -> PublishRecordSummary:
        return PublishRecordSummary(
            id=row["id"],
            content_item_id=row["content_item_id"],
            version_id=row["version_id"],
            platform=row["platform"],
            published_at=datetime.fromisoformat(row["published_at"]),
            views=int(row["views"] or 0),
            inquiry_count=int(row["inquiry_count"] or 0),
            conversion_count=int(row["conversion_count"] or 0),
        )

    def get_next_post_recommendation(self, user_id: str) -> NextPostRecommendationSummary:
        with get_conn() as conn:
            best = conn.execute("SELECT id, label, summary FROM learned_patterns WHERE user_id = ? AND current_status = 'validated' ORDER BY confidence DESC LIMIT 1", (user_id,)).fetchone()
            bm = conn.execute("SELECT id, account_name FROM benchmark_accounts WHERE user_id = ? ORDER BY updated_at DESC LIMIT 2", (user_id,)).fetchall()
        refs = [str(x["id"]) for x in bm]
        return NextPostRecommendationSummary(
            recommended_topic="用一个真实咨询案例解释你是怎么定位问题并给出方案",
            recommended_pillar=(best["label"] if best else "咨询策略"),
            recommended_content_type="案例拆解",
            benchmark_reference_ids=refs,
            why_this_now="当前改造重点是把流量转成咨询，这条内容能同时做信任与承接。",
            expected_goal="咨询",
            recommended_hook_direction="开场直接点出目标用户常见卡点",
            recommended_conversion_direction="结尾给出私信关键词和评论区承接动作",
            do_not_do="不要只讲方法论，不给具体案例"
        )


content_studio_service = ContentStudioService()
