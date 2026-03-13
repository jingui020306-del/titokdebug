from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.schemas.rewrite_engine import RewriteHistoryItem, RewriteInput, RewriteReport, RewriteVariant


class RewriteEngineService:
    def create_mock(self, user_id: str, payload: RewriteInput) -> str:
        job_id = f"rw_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()

        with get_conn() as conn:
            conn.execute(
                "INSERT INTO rewrite_engine_jobs (id, user_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (job_id, user_id, "created", now, now),
            )

        report = self._build_report(job_id, payload)
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO rewrite_engine_reports (id, job_id, user_id, payload_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (f"rwr_{uuid.uuid4().hex[:10]}", job_id, user_id, json.dumps(report.model_dump(mode="json"), ensure_ascii=False), now),
            )
            conn.execute("UPDATE rewrite_engine_jobs SET status = ?, updated_at = ? WHERE id = ?", ("ready", now, job_id))
        return job_id

    def get_report(self, job_id: str, user_id: str) -> RewriteReport | None:
        with get_conn() as conn:
            row = conn.execute(
                """
                SELECT r.payload_json
                FROM rewrite_engine_reports r
                JOIN rewrite_engine_jobs j ON j.id = r.job_id
                WHERE r.job_id = ? AND j.user_id = ?
                ORDER BY r.created_at DESC LIMIT 1
                """,
                (job_id, user_id),
            ).fetchone()
        if not row:
            return None
        return RewriteReport(**json.loads(row["payload_json"]))

    def get_history(self, user_id: str) -> list[RewriteHistoryItem]:
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT j.id AS job_id, j.status, j.created_at, r.payload_json
                FROM rewrite_engine_jobs j
                LEFT JOIN rewrite_engine_reports r ON r.job_id = j.id
                WHERE j.user_id = ?
                ORDER BY j.created_at DESC
                """,
                (user_id,),
            ).fetchall()

        items: list[RewriteHistoryItem] = []
        for row in rows:
            platform = "-"
            goal = "-"
            if row["payload_json"]:
                raw = json.loads(row["payload_json"])
                inp = raw.get("rewrite_input", {})
                platform = inp.get("platform", "-")
                goal = inp.get("goal", "-")
            items.append(
                RewriteHistoryItem(
                    job_id=row["job_id"],
                    status=row["status"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    platform=platform,
                    goal=goal,
                )
            )
        return items

    def _build_report(self, job_id: str, payload: RewriteInput) -> RewriteReport:
        title_variants = [
            RewriteVariant(label="A", content=f"别再硬拍了：{payload.industry}账号 7 天起量的 3 个动作", rationale="问题导向 + 时间承诺 + 数字结构"),
            RewriteVariant(label="B", content=f"{payload.target_audience}最容易忽略的一个增长杠杆（实操版）", rationale="人群点名 + 缺口提示"),
            RewriteVariant(label="C", content=f"同样内容，为什么你没结果？先改这 1 个开头", rationale="对比冲突 + 强钩子"),
        ]
        cover_variants = [
            RewriteVariant(label="A", content="先改开头，再谈增长", rationale="短句强指令，适合抖音封面识别"),
            RewriteVariant(label="B", content="这3句不改，流量很难稳", rationale="结果预警型，更适合小红书收藏心智"),
        ]
        hook_variants = [
            RewriteVariant(label="A", content="你这条视频不是内容差，是开头把人劝退了。", rationale="先给结论，提升停留"),
            RewriteVariant(label="B", content="同样主题，有人涨粉有人没播放，差在第1句。", rationale="对比驱动继续观看"),
            RewriteVariant(label="C", content="如果你最近有播放不涨粉，先检查这3个口播动作。", rationale="直击痛点 + 结构预告"),
        ]

        return RewriteReport(
            job_id=job_id,
            created_at=datetime.now(timezone.utc),
            rewrite_input=payload,
            report_title=f"{payload.industry}改稿执行方案",
            preview_text="优先重写标题与前3秒钩子，再统一结尾CTA，提升转化承接。",
            recommended_next_module="account_audit",
            diagnosis_summary="原稿信息点有价值，但标题过平、前3秒进入慢、结尾缺动作指令，导致流量承接和转化不足。",
            title_variants=title_variants,
            cover_variants=cover_variants,
            hook_variants=hook_variants,
            body_script="正文建议改成‘问题定义 -> 常见误区 -> 三步动作 -> 真实结果预期 -> 反例提醒’五段，段间加入一句话过桥，避免口播跳段。",
            closing_cta="如果你要我按你的行业做一版可直接拍的脚本，评论区打“改稿”，我按高频问题继续拆。",
            comment_guide="置顶评论：你的账号现在是“没播放 / 不涨粉 / 不转化”哪一种？我按问题类型给你发对应模板。",
            risk_replacements=[
                {"raw": "保证涨粉", "safe": "更有机会提升关注转化"},
                {"raw": "必火", "safe": "更符合平台分发偏好"},
                {"raw": "立刻变现", "safe": "更容易形成有效咨询线索"},
            ],
            recommended_use_case={
                "douyin": "优先使用标题A + 封面A + 钩子A，强调短时强抓取。",
                "xiaohongshu": "优先使用标题B + 封面B + 钩子C，强化收藏与评论讨论。",
            },
        )


rewrite_engine_service = RewriteEngineService()
