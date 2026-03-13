from __future__ import annotations

from datetime import datetime, timezone

from app.core.config import get_settings
from app.core.db import get_conn
from app.schemas.user import AnalysisRecord, MeOverview, UserProfile


class UserService:
    def ensure_user(self, user_id: str, display_name: str, email: str) -> UserProfile:
        now = datetime.now(timezone.utc).isoformat()
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row:
                conn.execute(
                    "UPDATE users SET display_name = ?, email = ?, updated_at = ? WHERE id = ?",
                    (display_name, email, now, user_id),
                )
                created_at = row["created_at"]
            else:
                conn.execute(
                    "INSERT INTO users (id, display_name, email, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, display_name, email, now, now),
                )
                created_at = now

        return UserProfile(id=user_id, display_name=display_name, email=email, created_at=datetime.fromisoformat(created_at))

    def get_user(self, user_id: str) -> UserProfile:
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not row:
            raise KeyError(user_id)
        return UserProfile(
            id=row["id"],
            display_name=row["display_name"],
            email=row["email"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def get_overview(self, user_id: str) -> MeOverview:
        user = self.get_user(user_id)
        settings = get_settings()

        with get_conn() as conn:
            audit_count = conn.execute("SELECT COUNT(1) AS c FROM account_audit_jobs WHERE user_id = ?", (user_id,)).fetchone()["c"]
            niche_count = conn.execute("SELECT COUNT(1) AS c FROM niche_map_jobs WHERE user_id = ?", (user_id,)).fetchone()["c"]
            rewrite_count = conn.execute("SELECT COUNT(1) AS c FROM rewrite_engine_jobs WHERE user_id = ?", (user_id,)).fetchone()["c"]

            rows = conn.execute(
                """
                SELECT module, job_id, status, created_at
                FROM (
                    SELECT 'account-audit' AS module, id AS job_id, status, created_at FROM account_audit_jobs WHERE user_id = ?
                    UNION ALL
                    SELECT 'niche-map' AS module, id AS job_id, status, created_at FROM niche_map_jobs WHERE user_id = ?
                    UNION ALL
                    SELECT 'rewrite-engine' AS module, id AS job_id, status, created_at FROM rewrite_engine_jobs WHERE user_id = ?
                ) t
                ORDER BY created_at DESC
                LIMIT 8
                """,
                (user_id, user_id, user_id),
            ).fetchall()

        records = [
            AnalysisRecord(module=row["module"], job_id=row["job_id"], status=row["status"], created_at=datetime.fromisoformat(row["created_at"]))
            for row in rows
        ]

        return MeOverview(
            user=user,
            account_audit_count=int(audit_count),
            niche_map_count=int(niche_count),
            rewrite_engine_count=int(rewrite_count),
            provider_mode=settings.default_provider_mode,
            last_analysis_at=records[0].created_at if records else None,
            recent_records=records,
        )


user_service = UserService()
