from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.schemas.review_lab import ReviewCreateRequest, ReviewHistoryItem, ReviewReport


class ReviewLabService:
    def create_review(self, user_id: str, payload: ReviewCreateRequest) -> str:
        review_id = f"rv_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc)

        bottleneck = self._detect_bottleneck(payload)
        decision = self._decision(payload)
        suggested = "content_studio" if bottleneck in {"留存", "承接"} else "positioning"

        prev = self._get_previous_review(user_id, payload)
        prev_delta = self._build_previous_delta(prev, payload)
        compare = self._build_comparison(user_id, payload, prev, decision)

        report = ReviewReport(
            review_id=review_id,
            created_at=now,
            report_title="复盘台本次结论",
            preview_text="本轮复盘已定位核心瓶颈，并生成下一轮可执行动作。",
            recommended_next_module=suggested,
            performance_summary="本条内容已有基础曝光，但转化链路仍有可优化空间。",
            self_comparison=compare["comparison_summary"],
            pillar_comparison=str(compare["pillar_benchmark"].get("current_item_vs_pillar_average", "暂无")),
            benchmark_comparison="已对照强账号模式给出差距与改法。",
            best_account_playbook_match="当前更接近“先结论后证据”的咨询承接 playbook。",
            content_type_assessment="案例拆解题型更接近高咨询样本，建议继续放大。",
            consultation_performance_summary=self._consultation_summary(payload),
            upgrade_progress_assessment="若连续两轮无改善，建议回定位台；当前可继续在内容台迭代。",
            decision={
                "problem_level": "high" if bottleneck in {"曝光", "承接"} else "medium",
                "recommended_action": decision,
                "reason": self._diagnosis(bottleneck),
                "benchmark_learning_status": "正在模仿" if decision == "继续测试" else "已初步贴近",
            },
            next_iteration_actions=["重写结尾 CTA，明确咨询动作", "发布后 2 小时内集中回复高价值评论", "补一条案例拆解作为承接内容"],
            linked_content_context={
                "current_status": "reviewed",
                "content_pillar": payload.content_pillar,
                "rewrite_version": payload.version_id or payload.rewrite_version or "未标注",
                "published_at": payload.publish_time.isoformat(),
            },
            comparison_summary=compare["comparison_summary"],
            previous_version_comparison=compare["previous_version_comparison"],
            pillar_benchmark=compare["pillar_benchmark"],
            strategy_window_comparison=compare["strategy_window_comparison"],
            consultation_quality_signal=self._consultation_quality_signal(payload),
            conversion_readiness_assessment=self._conversion_readiness(payload),
        )

        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO review_entries (id, user_id, source_type, payload_json, report_json, content_item_id, publish_record_id, version_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    review_id,
                    user_id,
                    payload.source_type,
                    json.dumps(payload.model_dump(mode="json"), ensure_ascii=False),
                    json.dumps(report.model_dump(mode="json"), ensure_ascii=False),
                    payload.content_item_id,
                    payload.publish_record_id,
                    payload.version_id or payload.rewrite_version,
                    now.isoformat(),
                    now.isoformat(),
                ),
            )
            conn.execute(
                "INSERT INTO learned_patterns (id, user_id, pattern_type, pattern_text, score, label, summary, evidence_source, confidence, current_status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    f"lp_{uuid.uuid4().hex[:10]}",
                    user_id,
                    self._pattern_type_from_bottleneck(bottleneck),
                    report.next_iteration_actions[0],
                    75,
                    f"{payload.content_pillar}优化动作",
                    report.next_iteration_actions[0],
                    f"review:{review_id}",
                    75,
                    "candidate" if decision == "继续测试" else "validated",
                    now.isoformat(),
                    now.isoformat(),
                ),
            )
            if payload.content_item_id:
                conn.execute(
                    "UPDATE content_items SET status = 'reviewed', latest_review_id = ?, updated_at = ? WHERE id = ? AND user_id = ?",
                    (review_id, now.isoformat(), payload.content_item_id, user_id),
                )
            if payload.rewrite_version:
                conn.execute("UPDATE content_iterations SET status = 'reviewed' WHERE user_id = ? AND rewrite_job_id = ?", (user_id, payload.rewrite_version))
        return review_id

    def get_report(self, user_id: str, review_id: str) -> ReviewReport | None:
        with get_conn() as conn:
            row = conn.execute("SELECT report_json FROM review_entries WHERE id = ? AND user_id = ?", (review_id, user_id)).fetchone()
        if not row:
            return None
        return ReviewReport(**json.loads(row["report_json"]))

    def history(self, user_id: str, pillar: str | None = None) -> list[ReviewHistoryItem]:
        with get_conn() as conn:
            rows = conn.execute("SELECT id, created_at, payload_json, report_json FROM review_entries WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        items: list[ReviewHistoryItem] = []
        for row in rows:
            payload = json.loads(row["payload_json"])
            if pillar and payload.get("content_pillar") != pillar:
                continue
            report = json.loads(row["report_json"])
            compare = str((report.get("previous_version_comparison") or {}).get("interpretation", "暂无可比数据"))
            items.append(
                ReviewHistoryItem(
                    review_id=row["id"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    content_title=payload.get("content_title", "未命名内容"),
                    content_pillar=payload.get("content_pillar", "未分类"),
                    major_metrics=f"播放{payload.get('views',0)} / 点赞{payload.get('likes',0)} / 咨询{payload.get('inquiry_count',0)} / 成单{payload.get('conversion_count',0)}",
                    comparison_signal=compare,
                    worth_scaling="值得放大" if str((report.get("decision") or {}).get("recommended_action", "")) == "放大" else "先继续测试",
                    decision=str((report.get("decision") or {}).get("recommended_action", "继续测试")),
                    next_action=(report.get("next_iteration_actions") or ["继续观察"])[0],
                    pattern_impact="已沉淀" if str((report.get("decision") or {}).get("recommended_action", "")) in {"放大", "停止此方向"} else "候选中",
                )
            )
        return items

    def _get_previous_review(self, user_id: str, payload: ReviewCreateRequest) -> dict | None:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT payload_json, report_json FROM review_entries WHERE user_id = ? ORDER BY created_at DESC LIMIT 20",
                (user_id,),
            ).fetchall()
        for r in rows:
            p = json.loads(r["payload_json"])
            if payload.content_item_id and p.get("content_item_id") == payload.content_item_id:
                return {"payload": p, "report": json.loads(r["report_json"])}
            if p.get("content_title") == payload.content_title:
                return {"payload": p, "report": json.loads(r["report_json"])}
        return None

    def _build_comparison(self, user_id: str, payload: ReviewCreateRequest, previous: dict | None, decision: str) -> dict:
        prev_payload = previous["payload"] if previous else {}
        prev_version_id = str(prev_payload.get("version_id") or prev_payload.get("rewrite_version") or "")
        changed_fields: list[str] = []
        if prev_version_id and prev_version_id != (payload.version_id or payload.rewrite_version or ""):
            changed_fields.append("版本")
        if prev_payload.get("content_title") != payload.content_title:
            changed_fields.append("标题")

        with get_conn() as conn:
            pstats = conn.execute(
                "SELECT AVG(views) as av, AVG(inquiry_count) as ai, AVG(conversion_count) as ac FROM publish_records WHERE content_item_id IN (SELECT id FROM content_items WHERE user_id = ? AND pillar = ?)",
                (user_id, payload.content_pillar),
            ).fetchone()
            window = conn.execute(
                "SELECT AVG(inquiry_count) as ai, AVG(views) as av FROM publish_records p JOIN content_items c ON c.id = p.content_item_id WHERE c.user_id = ? ORDER BY p.published_at DESC LIMIT 10",
                (user_id,),
            ).fetchone()

        prev_vs = {
            "previous_version_id": prev_version_id or "暂无可对比版本",
            "changed_fields": "、".join(changed_fields) if changed_fields else "暂无显著改动",
            "metric_deltas": f"播放{payload.views - int(prev_payload.get('views', 0)):+d} / 咨询{payload.inquiry_count - int(prev_payload.get('inquiry_count', 0)):+d}",
            "interpretation": "较上一版更好" if payload.inquiry_count >= int(prev_payload.get("inquiry_count", 0)) else "较上一版更弱",
        }
        pillar_avg_views = float(pstats["av"] or 0)
        pillar_avg_inquiry = float(pstats["ai"] or 0)
        strategy_avg_views = float(window["av"] or 0)
        strategy_avg_inquiry = float(window["ai"] or 0)
        pillar_cmp = {
            "current_pillar": payload.content_pillar,
            "pillar_average_summary": f"同支柱平均播放{pillar_avg_views:.0f}，平均咨询{pillar_avg_inquiry:.1f}",
            "current_item_vs_pillar_average": "高于平均" if payload.inquiry_count >= pillar_avg_inquiry else "低于平均",
            "whether_this_pillar_is_worth_scaling": decision == "放大",
        }
        window_cmp = {
            "recent_window_size": 10,
            "current_item_vs_recent_average": f"播放差值 {payload.views - int(strategy_avg_views):+d}",
            "current_item_vs_recent_consultation_average": f"咨询差值 {payload.inquiry_count - int(strategy_avg_inquiry):+d}",
            "conclusion": "可放大" if decision == "放大" else "继续测试",
        }
        return {
            "comparison_summary": f"相较上一版，当前在咨询承接上{prev_vs['interpretation']}，当前建议：{decision}。",
            "previous_version_comparison": prev_vs,
            "pillar_benchmark": pillar_cmp,
            "strategy_window_comparison": window_cmp,
        }

    @staticmethod
    def _detect_bottleneck(payload: ReviewCreateRequest) -> str:
        if payload.views < 2000:
            return "曝光"
        if payload.likes + payload.comments < max(10, payload.views * 0.02):
            return "留存"
        if payload.profile_visits < max(5, payload.views * 0.005):
            return "涨粉"
        return "承接"

    @staticmethod
    def _decision(payload: ReviewCreateRequest) -> str:
        if payload.conversion_count >= 1:
            return "放大"
        if payload.inquiry_count >= 2:
            return "继续测试"
        if payload.views < 1200 and payload.inquiry_count == 0:
            return "停止此方向"
        return "继续测试"

    @staticmethod
    def _diagnosis(stage: str) -> str:
        mapping = {
            "曝光": "平台分发入口弱，标题与封面识别度不足。",
            "留存": "前3秒钩子弱，用户停留不足导致后续动作断层。",
            "涨粉": "主页承接和身份表达不够明确，访问转关注偏低。",
            "承接": "咨询动作设计不足，评论区和私信链路不完整。",
        }
        return mapping.get(stage, "当前瓶颈需要进一步观察。")

    @staticmethod
    def _build_previous_delta(previous: dict | None, payload: ReviewCreateRequest) -> dict[str, str]:
        if not previous:
            return {"summary": "暂无可对比版本", "views_delta": "-", "consultation_delta": "-"}
        prev_payload = previous["payload"]
        vd = payload.views - int(prev_payload.get("views", 0))
        cd = payload.inquiry_count - int(prev_payload.get("inquiry_count") or 0)
        return {
            "summary": "与上一轮相比已更新一次策略动作",
            "views_delta": f"{vd:+d}",
            "consultation_delta": f"{cd:+d}",
        }

    @staticmethod
    def _pattern_type_from_bottleneck(stage: str) -> str:
        return {
            "曝光": "title_style",
            "留存": "hook_style",
            "涨粉": "profile_expression",
            "承接": "conversion_cta",
        }.get(stage, "pillar")

    @staticmethod
    def _consultation_summary(payload: ReviewCreateRequest) -> str:
        return f"私信{payload.dm_count}，咨询{payload.inquiry_count}，成单{payload.conversion_count}。"

    @staticmethod
    def _consultation_quality_signal(payload: ReviewCreateRequest) -> str:
        if payload.inquiry_count == 0 and payload.views > 5000:
            return "有流量但无咨询"
        if payload.inquiry_count > 0 and payload.conversion_count == 0:
            return "有咨询但不成单"
        if payload.inquiry_count <= 2 and payload.conversion_count >= 1:
            return "咨询少但精准"
        if payload.profile_visits > 0 and payload.inquiry_count == 0:
            return "涨粉有效但承接弱"
        return "咨询转化链路基本正常"

    @staticmethod
    def _conversion_readiness(payload: ReviewCreateRequest) -> str:
        if payload.conversion_count >= 1:
            return "当前版本具备可放大条件，建议继续沿同支柱迭代。"
        if payload.inquiry_count >= 1:
            return "有咨询信号，需优化咨询前置筛选和话术。"
        return "当前转化准备度不足，先优化钩子与承接动作。"


review_lab_service = ReviewLabService()
