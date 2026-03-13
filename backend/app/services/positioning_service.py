from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.schemas.common import PositioningVersionSummary


class PositioningService:
    def ensure_version_from_job(self, user_id: str, job_id: str) -> PositioningVersionSummary | None:
        with get_conn() as conn:
            report = conn.execute(
                "SELECT payload_json, created_at FROM audit_reports WHERE user_id = ? AND job_id = ? ORDER BY created_at DESC LIMIT 1",
                (user_id, job_id),
            ).fetchone()
            if not report:
                return None
            existing = conn.execute("SELECT * FROM positioning_versions WHERE user_id = ? AND job_id = ? LIMIT 1", (user_id, job_id)).fetchone()
            payload = json.loads(report["payload_json"])
            if existing:
                return self._row_to_summary(existing)
            latest_active = conn.execute("SELECT * FROM positioning_versions WHERE user_id = ? AND is_active = 1 LIMIT 1", (user_id,)).fetchone()
            change_level = self._detect_change_level(latest_active, payload)
            now = datetime.now(timezone.utc).isoformat()
            version_id = f"pv_{uuid.uuid4().hex[:10]}"
            conn.execute(
                """
                INSERT INTO positioning_versions
                (positioning_version_id, user_id, job_id, report_title, preview_text, is_active, is_frozen, frozen_at, supersedes_version_id, change_level, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version_id,
                    user_id,
                    job_id,
                    payload.get("report_title", "定位报告"),
                    payload.get("preview_text", "定位结论"),
                    1 if latest_active is None else 0,
                    0,
                    None,
                    latest_active["positioning_version_id"] if latest_active else None,
                    change_level,
                    report["created_at"],
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM positioning_versions WHERE positioning_version_id = ?", (version_id,)).fetchone()
        return self._row_to_summary(row)

    def freeze(self, user_id: str, job_id: str) -> bool:
        with get_conn() as conn:
            row = conn.execute("SELECT positioning_version_id FROM positioning_versions WHERE user_id = ? AND job_id = ? LIMIT 1", (user_id, job_id)).fetchone()
            if not row:
                return False
            now = datetime.now(timezone.utc).isoformat()
            conn.execute("UPDATE positioning_versions SET is_frozen = 1, frozen_at = ?, updated_at = ? WHERE positioning_version_id = ?", (now, now, row["positioning_version_id"]))
        return True

    def set_active(self, user_id: str, job_id: str) -> bool:
        with get_conn() as conn:
            row = conn.execute("SELECT positioning_version_id FROM positioning_versions WHERE user_id = ? AND job_id = ? LIMIT 1", (user_id, job_id)).fetchone()
            if not row:
                return False
            now = datetime.now(timezone.utc).isoformat()
            conn.execute("UPDATE positioning_versions SET is_active = 0, updated_at = ? WHERE user_id = ?", (now, user_id))
            conn.execute("UPDATE positioning_versions SET is_active = 1, updated_at = ? WHERE positioning_version_id = ?", (now, row["positioning_version_id"]))
        return True

    def get_active(self, user_id: str) -> PositioningVersionSummary | None:
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM positioning_versions WHERE user_id = ? AND is_active = 1 LIMIT 1", (user_id,)).fetchone()
        if not row:
            return None
        return self._row_to_summary(row)

    def list_versions(self, user_id: str) -> list[PositioningVersionSummary]:
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM positioning_versions WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        return [self._row_to_summary(r) for r in rows]

    def _detect_change_level(self, latest_active, payload: dict) -> str:
        if latest_active is None:
            return "minor"
        text = (payload.get("preview_text") or "")
        if "重做" in text or "转向" in text:
            return "major"
        if "调整" in text or "优化" in text:
            return "moderate"
        return "minor"

    @staticmethod
    def _row_to_summary(row) -> PositioningVersionSummary:
        return PositioningVersionSummary(
            positioning_version_id=row["positioning_version_id"],
            job_id=row["job_id"],
            report_title=row["report_title"],
            preview_text=row["preview_text"],
            is_active=bool(row["is_active"]),
            is_frozen=bool(row["is_frozen"]),
            frozen_at=datetime.fromisoformat(row["frozen_at"]) if row["frozen_at"] else None,
            supersedes_version_id=row["supersedes_version_id"],
            change_level=row["change_level"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )


positioning_service = PositioningService()
