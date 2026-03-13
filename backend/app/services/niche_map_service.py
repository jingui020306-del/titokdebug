from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.schemas.niche_map import NicheInput, NicheMapHistoryItem, NicheMapReport


class NicheMapService:
    def create_mock(self, user_id: str, payload: NicheInput) -> str:
        job_id = f"nm_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO niche_map_jobs (id, user_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (job_id, user_id, "created", now, now),
            )

        report = self._build_report(job_id, payload)
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO niche_map_reports (id, job_id, user_id, payload_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (f"nmr_{uuid.uuid4().hex[:10]}", job_id, user_id, json.dumps(report.model_dump(mode='json'), ensure_ascii=False), now),
            )
            conn.execute(
                "UPDATE niche_map_jobs SET status = ?, updated_at = ? WHERE id = ?",
                ("ready", now, job_id),
            )
        return job_id

    def get_report(self, job_id: str, user_id: str) -> NicheMapReport | None:
        with get_conn() as conn:
            row = conn.execute(
                """
                SELECT r.payload_json
                FROM niche_map_reports r
                JOIN niche_map_jobs j ON j.id = r.job_id
                WHERE r.job_id = ? AND j.user_id = ?
                ORDER BY r.created_at DESC LIMIT 1
                """,
                (job_id, user_id),
            ).fetchone()
        if not row:
            return None
        return NicheMapReport(**json.loads(row["payload_json"]))

    def get_history(self, user_id: str) -> list[NicheMapHistoryItem]:
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT j.id as job_id, j.status, j.created_at, r.payload_json
                FROM niche_map_jobs j
                LEFT JOIN niche_map_reports r ON r.job_id = j.id
                WHERE j.user_id = ?
                ORDER BY j.created_at DESC
                """,
                (user_id,),
            ).fetchall()
        items: list[NicheMapHistoryItem] = []
        for row in rows:
            platform = "-"
            niche_keyword = "-"
            if row["payload_json"]:
                payload = json.loads(row["payload_json"])
                niche_input = payload.get("niche_input", {})
                platform = niche_input.get("platform", "-")
                niche_keyword = niche_input.get("niche_keyword", "-")
            items.append(
                NicheMapHistoryItem(
                    job_id=row["job_id"],
                    status=row["status"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    platform=platform,
                    niche_keyword=niche_keyword,
                )
            )
        return items

    def _build_report(self, job_id: str, payload: NicheInput) -> NicheMapReport:
        return NicheMapReport(
            job_id=job_id,
            created_at=datetime.now(timezone.utc),
            niche_input=payload,
            report_title=f"{payload.niche_keyword}赛道地图 V1",
            preview_text="赛道竞争已分层，建议先从低成本高信任的案例拆解切入。",
            recommended_next_module="rewrite_engine",
            market_summary=f"{payload.platform} 的「{payload.niche_keyword}」赛道已进入中度竞争阶段，纯信息搬运内容增长放缓，案例化与实操化内容仍有窗口。",
            audience_insights=[
                f"目标用户（{payload.target_audience}）更愿意为“可直接照做”的方法停留。",
                "用户在评论区最常追问的是“具体怎么开始”和“投入产出比”。",
                "对“踩坑复盘 + 可复制模板”类内容互动更高。",
            ],
            competitor_layers=[
                {"layer": "头部（100w+）", "feature": "强人设 + 系列栏目 + 高频直播承接"},
                {"layer": "腰部（10w-100w）", "feature": "案例拆解稳定，标题与封面风格统一"},
                {"layer": "成长型（1w-10w）", "feature": "内容质量可用，但定位表达和变现链路弱"},
            ],
            winning_formats=[
                {"format": "反常识开场 + 三步拆解", "evidence": "近 30 天同赛道高互动内容常见结构"},
                {"format": "真实案例前后对比", "evidence": "用户更愿意收藏并转发给团队"},
                {"format": "清单模板型", "evidence": "私域导流与咨询转化效率更高"},
            ],
            suggested_entry_points=[
                "从“{0}最容易犯的3个错误”切入，降低理解门槛。".format(payload.niche_keyword),
                "围绕你的服务/产品做“场景化拆解”，避免泛干货。",
                "先做 14 天同主题栏目，建立稳定标签。",
            ],
            avoid_directions=[
                "不要直接复制头部账号的选题节奏，成本高且辨识度低。",
                "不要做过宽话题（如‘全行业增长’），很难形成精准受众。",
                "不要提前重商业化内容比重，先稳定互动与关注。",
            ],
            recommended_pillars=[
                {"pillar": "赛道机会识别", "why": "让用户看到“为什么现在做”。"},
                {"pillar": "案例拆解", "why": "用证据建立信任与专业度。"},
                {"pillar": "执行模板", "why": "帮助用户立刻上手，提高收藏和转化。"},
            ],
            monetization_paths=[
                f"先用公开内容吸引 {payload.goal} 人群，再以咨询/训练营承接。",
                "用“诊断清单+复盘服务”做低门槛试单，再升级长期服务。",
            ],
            recommended_next_step="go_rewrite_engine",
        )


niche_map_service = NicheMapService()
