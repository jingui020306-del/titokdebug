from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.schemas.review_lab import (
    AccountUpgradePlan,
    BenchmarkAccountSummary,
    BenchmarkContentSample,
    BenchmarkCreateRequest,
    BenchmarkGapItem,
    BenchmarkGapSummary,
    BenchmarkPatchRequest,
    BenchmarkPlaybook,
    BenchmarkSampleCreateRequest,
    DiscoveryCandidate,
    DiscoverySearchRequest,
)


class BenchmarkService:
    def discovery_search(self, user_id: str, payload: DiscoverySearchRequest) -> list[DiscoveryCandidate]:
        return [
            DiscoveryCandidate(
                account_name=f"{payload.niche_keyword}头部样本A",
                platform="抖音",
                account_url="https://www.douyin.com/user/mock_head_a",
                similarity_reason="服务对象与你接近，表达方式同为咨询型内容。",
                learnability_reason="标题钩子稳定，咨询承接动作清晰可复制。",
                learn_target=payload.learning_preference,
                should_add=True,
            ),
            DiscoveryCandidate(
                account_name=f"{payload.niche_keyword}同阶段样本B",
                platform="抖音",
                account_url="https://www.douyin.com/user/mock_peer_b",
                similarity_reason="赛道关键词与目标用户重合，内容结构相似。",
                learnability_reason="发布节奏与题型分配可直接借鉴。",
                learn_target="更稳咨询",
                should_add=True,
            ),
        ]

    def create_benchmark(self, user_id: str, payload: BenchmarkCreateRequest) -> BenchmarkAccountSummary:
        now = datetime.now(timezone.utc)
        bid = f"bm_{uuid.uuid4().hex[:10]}"
        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO benchmark_accounts
                (id, user_id, account_name, platform, account_url, niche_label, account_tier, similarity_reason, learnability_reason, positioning_summary, why_selected, notes, source_mode, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    bid,
                    user_id,
                    payload.account_name,
                    payload.platform,
                    payload.account_url,
                    payload.niche_label,
                    payload.account_tier,
                    payload.similarity_reason,
                    payload.learnability_reason,
                    payload.positioning_summary,
                    payload.why_selected,
                    payload.notes,
                    payload.source_mode,
                    now.isoformat(),
                    now.isoformat(),
                ),
            )
            # bootstrap a playbook
            conn.execute(
                "INSERT INTO benchmark_playbooks (id, benchmark_account_id, playbook_type, summary, evidence_source, confidence, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (f"bp_{uuid.uuid4().hex[:10]}", bid, "hook", "开场先给结论再给证据链，咨询转化更稳定。", "sample:bootstrap", 78, now.isoformat(), now.isoformat()),
            )
        return self.get_benchmark(user_id, bid)

    def confirm_candidates(self, user_id: str, candidates: list[DiscoveryCandidate]) -> list[BenchmarkAccountSummary]:
        created: list[BenchmarkAccountSummary] = []
        for c in candidates:
            if not c.should_add:
                continue
            created.append(
                self.create_benchmark(
                    user_id,
                    BenchmarkCreateRequest(
                        account_name=c.account_name,
                        platform=c.platform,
                        account_url=c.account_url,
                        account_tier="peer",
                        similarity_reason=c.similarity_reason,
                        learnability_reason=c.learnability_reason,
                        positioning_summary=f"聚焦{c.learn_target}",
                        why_selected=f"系统推荐：{c.learn_target}",
                        source_mode="discovered",
                    ),
                )
            )
        return created

    def list_benchmarks(self, user_id: str) -> list[BenchmarkAccountSummary]:
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM benchmark_accounts WHERE user_id = ? ORDER BY updated_at DESC", (user_id,)).fetchall()
        return [self._row_to_benchmark(r) for r in rows]

    def get_benchmark(self, user_id: str, benchmark_id: str) -> BenchmarkAccountSummary:
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM benchmark_accounts WHERE id = ? AND user_id = ?", (benchmark_id, user_id)).fetchone()
        if not row:
            raise KeyError(benchmark_id)
        return self._row_to_benchmark(row)

    def patch_benchmark(self, user_id: str, benchmark_id: str, payload: BenchmarkPatchRequest) -> BenchmarkAccountSummary:
        fields = []
        vals: list[object] = []
        if payload.notes is not None:
            fields.append("notes = ?")
            vals.append(payload.notes)
        if payload.why_selected is not None:
            fields.append("why_selected = ?")
            vals.append(payload.why_selected)
        if payload.account_tier is not None:
            fields.append("account_tier = ?")
            vals.append(payload.account_tier)
        if fields:
            vals.extend([datetime.now(timezone.utc).isoformat(), benchmark_id, user_id])
            with get_conn() as conn:
                conn.execute(f"UPDATE benchmark_accounts SET {', '.join(fields)}, updated_at = ? WHERE id = ? AND user_id = ?", tuple(vals))
        return self.get_benchmark(user_id, benchmark_id)

    def list_samples(self, user_id: str, benchmark_id: str) -> list[BenchmarkContentSample]:
        _ = self.get_benchmark(user_id, benchmark_id)
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM benchmark_content_samples WHERE benchmark_account_id = ? ORDER BY updated_at DESC", (benchmark_id,)).fetchall()
        return [self._row_to_sample(r) for r in rows]

    def create_sample(self, user_id: str, benchmark_id: str, payload: BenchmarkSampleCreateRequest) -> BenchmarkContentSample:
        _ = self.get_benchmark(user_id, benchmark_id)
        sid = f"bs_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc)
        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO benchmark_content_samples
                (id, benchmark_account_id, title, sample_url, content_type, pillar_guess, hook_style, conversion_style, sample_heat_level, sample_notes, metrics_snapshot_text, publish_date_text, why_it_worked, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sid,
                    benchmark_id,
                    payload.title,
                    payload.sample_url,
                    payload.content_type,
                    payload.pillar_guess,
                    payload.hook_style,
                    payload.conversion_style,
                    payload.sample_heat_level,
                    payload.sample_notes,
                    payload.metrics_snapshot_text,
                    payload.publish_date_text,
                    payload.why_it_worked,
                    now.isoformat(),
                    now.isoformat(),
                ),
            )
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM benchmark_content_samples WHERE id = ?", (sid,)).fetchone()
        return self._row_to_sample(row)

    def list_playbooks(self, user_id: str, benchmark_id: str) -> list[BenchmarkPlaybook]:
        _ = self.get_benchmark(user_id, benchmark_id)
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM benchmark_playbooks WHERE benchmark_account_id = ? ORDER BY confidence DESC", (benchmark_id,)).fetchall()
        return [self._row_to_playbook(r) for r in rows]

    def build_gap_to_action(self, user_id: str, review_id: str) -> tuple[BenchmarkGapSummary, AccountUpgradePlan]:
        with get_conn() as conn:
            review = conn.execute("SELECT payload_json FROM review_entries WHERE id = ? AND user_id = ?", (review_id, user_id)).fetchone()
            bm = conn.execute("SELECT id, account_name FROM benchmark_accounts WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1", (user_id,)).fetchone()
        if not review or not bm:
            raise KeyError(review_id)
        items = [
            BenchmarkGapItem(dimension="定位表达", my_current_state="定位句偏泛", benchmark_state="开场10秒明确身份与服务对象", gap_level="high", why_gap_exists="开场信息密度不足", suggested_change="开场先说服务对象+结果", urgency="now"),
            BenchmarkGapItem(dimension="咨询承接方式", my_current_state="结尾咨询动作弱", benchmark_state="评论区+私信双承接", gap_level="high", why_gap_exists="缺少明确承接指令", suggested_change="结尾固定加入咨询触发句", urgency="this_week"),
        ]
        gap = BenchmarkGapSummary(benchmark_account_id=bm["id"], items=items)
        plan = AccountUpgradePlan(
            what_to_keep=["继续保留案例拆解风格"],
            what_to_change_now=["主页一句话定位改成服务对象+问题+结果", "结尾固定咨询承接动作"],
            what_to_change_later=["逐步增加直播承接场景"],
            what_not_to_copy=["不要照抄头部账号的高频激进标题"],
            profile_upgrade_plan=["昵称增加细分领域标签", "简介增加咨询入口与服务边界", "主页headline写清可解决的问题"],
            content_structure_upgrade_plan=["支柱从4个收敛到3个", "减少泛经验输出，增加可执行清单"],
            content_type_upgrade_plan=["增加对比型题型", "暂停纯观点型空泛输出"],
            conversion_upgrade_plan=["评论区置顶咨询话术", "结尾加入低门槛咨询动作", "咨询型内容与涨粉型内容分流"],
            next_7_post_strategy=[
                {"title_direction": f"第{i+1}条：围绕{('定位表达' if i<3 else '咨询承接')}改造", "pillar": "咨询策略", "content_type": "案例拆解", "benchmark_reference": bm["account_name"], "why_now": "对应当前最大差距", "goal": "咨询", "do_not_do": "不要空泛讲道理", "next_step": "content_studio.rewrite"}
                for i in range(7)
            ],
        )
        return gap, plan

    @staticmethod
    def _row_to_benchmark(row) -> BenchmarkAccountSummary:
        return BenchmarkAccountSummary(
            id=row["id"], user_id=row["user_id"], account_name=row["account_name"], platform=row["platform"], account_url=row["account_url"], niche_label=row["niche_label"], account_tier=row["account_tier"],
            similarity_reason=row["similarity_reason"] or "", learnability_reason=row["learnability_reason"] or "", positioning_summary=row["positioning_summary"] or "", why_selected=row["why_selected"] or "", notes=row["notes"], source_mode=row["source_mode"],
            created_at=datetime.fromisoformat(row["created_at"]), updated_at=datetime.fromisoformat(row["updated_at"])
        )

    @staticmethod
    def _row_to_sample(row) -> BenchmarkContentSample:
        return BenchmarkContentSample(
            id=row["id"], benchmark_account_id=row["benchmark_account_id"], title=row["title"], sample_url=row["sample_url"], content_type=row["content_type"] or "", pillar_guess=row["pillar_guess"] or "", hook_style=row["hook_style"] or "", conversion_style=row["conversion_style"] or "", sample_heat_level=row["sample_heat_level"], sample_notes=row["sample_notes"] or "", metrics_snapshot_text=row["metrics_snapshot_text"] or "", publish_date_text=row["publish_date_text"] or "", why_it_worked=row["why_it_worked"] or "", created_at=datetime.fromisoformat(row["created_at"]), updated_at=datetime.fromisoformat(row["updated_at"])
        )

    @staticmethod
    def _row_to_playbook(row) -> BenchmarkPlaybook:
        return BenchmarkPlaybook(
            id=row["id"], benchmark_account_id=row["benchmark_account_id"], playbook_type=row["playbook_type"], summary=row["summary"], evidence_source=row["evidence_source"] or "", confidence=int(row["confidence"] or 0), created_at=datetime.fromisoformat(row["created_at"]), updated_at=datetime.fromisoformat(row["updated_at"])
        )


benchmark_service = BenchmarkService()
