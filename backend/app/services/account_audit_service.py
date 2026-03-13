from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

from app.core.db import get_conn
from app.schemas.account_audit import (
    AccountAuditHistoryItem,
    AccountAuditJobItem,
    AccountMetrics,
    AccountProfile,
    DeepReport,
    FastReport,
    MockCreateRequest,
    PostSnapshot,
    SupplementRequest,
)
from app.tasks import build_report_body, job_queue


class AccountAuditService:
    def create_mock_job(self, user_id: str, payload: MockCreateRequest) -> str:
        account_id = self._upsert_account(user_id=user_id, payload=payload)
        job_id = f"job_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()

        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO account_audit_jobs (id, account_id, user_id, source_type, status, report_mode_available, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (job_id, account_id, user_id, payload.source_type, "created", json.dumps([]), now, now),
            )

        job_queue.enqueue(self._run_fast_pipeline, job_id)
        job_queue.enqueue(self._run_deep_pipeline, job_id)
        return job_id

    def create_seed_job(self, user_id: str) -> str:
        payload = MockCreateRequest(account_id="seed_dy_001", nickname="Seed演示账号", source_type="mock")
        return self.create_mock_job(user_id=user_id, payload=payload)

    def get_job(self, user_id: str, job_id: str) -> AccountAuditJobItem:
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM account_audit_jobs WHERE id = ? AND user_id = ?", (job_id, user_id)).fetchone()
        if not row:
            raise KeyError(job_id)
        return self._row_to_job_item(row)

    def get_history(self, user_id: str) -> list[AccountAuditHistoryItem]:
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT j.*, a.nickname AS account_nickname
                FROM account_audit_jobs j
                JOIN accounts a ON a.id = j.account_id
                WHERE a.user_id = ?
                ORDER BY j.created_at DESC
                """,
                (user_id,),
            ).fetchall()

        return [
            AccountAuditHistoryItem(
                **self._row_to_job_item(row).model_dump(),
                account_nickname=row["account_nickname"],
            )
            for row in rows
        ]

    def list_reports(self, user_id: str, job_id: str) -> list[dict[str, str | int]]:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT mode, version, created_at FROM audit_reports WHERE job_id = ? AND user_id = ? ORDER BY created_at DESC",
                (job_id, user_id),
            ).fetchall()
        return [dict(row) for row in rows]

    def rerun(self, job_id: str) -> None:
        self._set_job_status(job_id, "created", [])
        job_queue.enqueue(self._run_fast_pipeline, job_id)
        job_queue.enqueue(self._run_deep_pipeline, job_id)

    def add_supplement(self, user_id: str, job_id: str, payload: SupplementRequest) -> None:
        self._require_job_owner(user_id, job_id)
        self._save_job_meta(job_id, payload.model_dump())

    def get_report(self, user_id: str, job_id: str, mode: Literal["fast", "deep"]) -> FastReport | DeepReport | None:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT payload_json FROM audit_reports WHERE job_id = ? AND user_id = ? AND mode = ? ORDER BY version DESC LIMIT 1",
                (job_id, user_id, mode),
            ).fetchone()
        if not row:
            return None
        payload = json.loads(row["payload_json"])
        return FastReport(**payload) if mode == "fast" else DeepReport(**payload)


    def export_report_json(self, user_id: str, job_id: str) -> dict:
        deep = self.get_report(user_id, job_id, "deep")
        if deep:
            return deep.model_dump(mode="json")
        fast = self.get_report(user_id, job_id, "fast")
        if fast:
            return fast.model_dump(mode="json")
        raise KeyError(job_id)

    def _require_job_owner(self, user_id: str, job_id: str) -> None:
        with get_conn() as conn:
            row = conn.execute("SELECT id FROM account_audit_jobs WHERE id = ? AND user_id = ?", (job_id, user_id)).fetchone()
        if not row:
            raise KeyError(job_id)
    def _run_fast_pipeline(self, job_id: str) -> None:
        self._set_job_status(job_id, "syncing_fast", [])
        profile, metrics, posts = self._build_job_data(job_id)
        body = build_report_body(profile.nickname, deep=False, supplement=self._load_job_meta(job_id))
        report = FastReport(
            job_id=job_id,
            generated_at=datetime.now(timezone.utc),
            account_profile=profile,
            account_metrics=metrics,
            post_snapshots=posts,
            **body,
        )
        self._save_snapshots(job_id, profile, posts)
        self._save_report(job_id, "fast", report.model_dump(mode="json"))
        self._set_job_status(job_id, "fast_ready", ["fast"])

    def _run_deep_pipeline(self, job_id: str) -> None:
        self._set_job_status(job_id, "syncing_deep", ["fast"])
        profile, metrics, posts = self._build_job_data(job_id)
        body = build_report_body(profile.nickname, deep=True, supplement=self._load_job_meta(job_id))
        report = DeepReport(
            job_id=job_id,
            generated_at=datetime.now(timezone.utc),
            account_profile=profile,
            account_metrics=metrics,
            post_snapshots=posts,
            **body,
        )
        self._save_report(job_id, "deep", report.model_dump(mode="json"))
        self._set_job_status(job_id, "deep_ready", ["fast", "deep"])

    def _upsert_account(self, user_id: str, payload: MockCreateRequest) -> str:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT id FROM accounts WHERE user_id = ? AND external_id = ?",
                (user_id, payload.account_id),
            ).fetchone()
            now = datetime.now(timezone.utc).isoformat()
            if row:
                conn.execute("UPDATE accounts SET nickname = ?, updated_at = ? WHERE id = ?", (payload.nickname, now, row["id"]))
                return row["id"]

            account_id = f"acct_{uuid.uuid4().hex[:10]}"
            conn.execute(
                """
                INSERT INTO accounts (id, user_id, source_type, external_id, nickname, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (account_id, user_id, payload.source_type, payload.account_id, payload.nickname, now, now),
            )
            return account_id

    def _set_job_status(self, job_id: str, status: str, modes: list[str]) -> None:
        with get_conn() as conn:
            conn.execute(
                "UPDATE account_audit_jobs SET status = ?, report_mode_available = ?, updated_at = ? WHERE id = ?",
                (status, json.dumps(modes), datetime.now(timezone.utc).isoformat(), job_id),
            )

    def _save_report(self, job_id: str, mode: str, payload: dict) -> None:
        with get_conn() as conn:
            vrow = conn.execute(
                "SELECT COALESCE(MAX(version), 0) as max_v FROM audit_reports WHERE job_id = ? AND mode = ?",
                (job_id, mode),
            ).fetchone()
            version = int(vrow["max_v"]) + 1
            conn.execute(
                """
                INSERT INTO audit_reports (id, job_id, user_id, report_type, mode, version, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"rep_{uuid.uuid4().hex[:10]}",
                    job_id,
                    self._get_job_user_id(job_id),
                    "account_audit",
                    mode,
                    version,
                    json.dumps(payload, ensure_ascii=False),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

    def _get_job_user_id(self, job_id: str) -> str:
        with get_conn() as conn:
            row = conn.execute("SELECT user_id FROM account_audit_jobs WHERE id = ?", (job_id,)).fetchone()
        if not row or not row["user_id"]:
            raise KeyError(job_id)
        return str(row["user_id"])

    def _save_snapshots(self, job_id: str, profile: AccountProfile, posts: list[PostSnapshot]) -> None:
        with get_conn() as conn:
            job = conn.execute("SELECT account_id FROM account_audit_jobs WHERE id = ?", (job_id,)).fetchone()
            if not job:
                return
            account_id = job["account_id"]
            conn.execute("DELETE FROM account_snapshots WHERE job_id = ?", (job_id,))
            conn.execute(
                """
                INSERT INTO account_snapshots (id, account_id, job_id, followers, following, bio, category, city, captured_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"as_{uuid.uuid4().hex[:10]}",
                    account_id,
                    job_id,
                    profile.followers,
                    profile.following,
                    profile.bio,
                    profile.category,
                    profile.city,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.execute("DELETE FROM post_snapshots WHERE job_id = ?", (job_id,))
            for post in posts:
                conn.execute(
                    """
                    INSERT INTO post_snapshots (id, job_id, post_id, title, topic, views, likes, comments, shares, publish_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"ps_{uuid.uuid4().hex[:10]}",
                        job_id,
                        post.post_id,
                        post.title,
                        post.topic,
                        post.views,
                        post.likes,
                        post.comments,
                        post.shares,
                        post.publish_time.isoformat(),
                    ),
                )

    def _save_job_meta(self, job_id: str, data: dict) -> None:
        with get_conn() as conn:
            conn.execute(
                "UPDATE account_audit_jobs SET error_message = ?, updated_at = ? WHERE id = ?",
                (json.dumps(data, ensure_ascii=False), datetime.now(timezone.utc).isoformat(), job_id),
            )

    def _load_job_meta(self, job_id: str) -> dict:
        with get_conn() as conn:
            row = conn.execute("SELECT error_message FROM account_audit_jobs WHERE id = ?", (job_id,)).fetchone()
        if row and row["error_message"]:
            try:
                return json.loads(row["error_message"])
            except json.JSONDecodeError:
                return {}
        return {}

    def _build_job_data(self, job_id: str) -> tuple[AccountProfile, AccountMetrics, list[PostSnapshot]]:
        with get_conn() as conn:
            row = conn.execute(
                """
                SELECT a.external_id, a.nickname
                FROM account_audit_jobs j
                JOIN accounts a ON a.id = j.account_id
                WHERE j.id = ?
                """,
                (job_id,),
            ).fetchone()
        if not row:
            raise KeyError(job_id)

        profile = AccountProfile(
            account_id=row["external_id"] or "unknown",
            nickname=row["nickname"],
            category="知识分享",
            city="杭州",
            followers=18620,
            following=113,
            bio="陪你把复杂问题讲简单，每周拆解增长案例",
        )
        metrics = AccountMetrics(
            post_count_30d=17,
            avg_views_30d=8421,
            avg_completion_rate_30d=0.322,
            avg_interaction_rate_30d=0.047,
            follow_convert_rate_30d=0.013,
        )
        now = datetime.now(timezone.utc)
        posts = [
            PostSnapshot(post_id="p_101", title="90天做出稳定更新节奏的3个动作", topic="创作方法", views=13200, likes=680, comments=72, shares=41, publish_time=now - timedelta(days=3)),
            PostSnapshot(post_id="p_102", title="定位总跑偏？先做这张选题过滤表", topic="定位策略", views=7900, likes=354, comments=39, shares=19, publish_time=now - timedelta(days=7)),
            PostSnapshot(post_id="p_103", title="一条口播怎么把完播率抬到35%", topic="口播脚本", views=6100, likes=241, comments=26, shares=12, publish_time=now - timedelta(days=10)),
        ]
        return profile, metrics, posts

    @staticmethod
    def _row_to_job_item(row) -> AccountAuditJobItem:
        modes = json.loads(row["report_mode_available"]) if row["report_mode_available"] else []
        return AccountAuditJobItem(
            id=row["id"],
            source_type=row["source_type"],
            status=row["status"],
            report_mode_available=modes,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )


account_audit_service = AccountAuditService()
