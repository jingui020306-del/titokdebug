from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "creator_os.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _add_column_if_missing(conn: sqlite3.Connection, table: str, column: str, column_ddl: str) -> None:
    cols = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column_ddl}")


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                source_type TEXT NOT NULL,
                external_id TEXT,
                nickname TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS account_audit_jobs (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                user_id TEXT,
                source_type TEXT NOT NULL,
                status TEXT NOT NULL,
                report_mode_available TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                error_message TEXT,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            );

            CREATE TABLE IF NOT EXISTS account_snapshots (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                job_id TEXT NOT NULL,
                followers INTEGER NOT NULL,
                following INTEGER NOT NULL,
                bio TEXT NOT NULL,
                category TEXT NOT NULL,
                city TEXT NOT NULL,
                captured_at TEXT NOT NULL,
                FOREIGN KEY(account_id) REFERENCES accounts(id),
                FOREIGN KEY(job_id) REFERENCES account_audit_jobs(id)
            );

            CREATE TABLE IF NOT EXISTS post_snapshots (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                post_id TEXT NOT NULL,
                title TEXT NOT NULL,
                topic TEXT NOT NULL,
                views INTEGER NOT NULL,
                likes INTEGER NOT NULL,
                comments INTEGER NOT NULL,
                shares INTEGER NOT NULL,
                publish_time TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES account_audit_jobs(id)
            );

            CREATE TABLE IF NOT EXISTS audit_reports (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                user_id TEXT,
                report_type TEXT NOT NULL,
                mode TEXT NOT NULL,
                version INTEGER NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES account_audit_jobs(id)
            );

            CREATE TABLE IF NOT EXISTS niche_map_jobs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS niche_map_reports (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                user_id TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES niche_map_jobs(id)
            );

            CREATE TABLE IF NOT EXISTS rewrite_engine_jobs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS rewrite_engine_reports (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                user_id TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES rewrite_engine_jobs(id)
            );

            CREATE TABLE IF NOT EXISTS content_plan_jobs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                status TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS review_entries (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                source_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                report_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS content_iterations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                rewrite_job_id TEXT,
                title TEXT NOT NULL,
                pillar TEXT NOT NULL,
                is_adopted INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'adopted',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS learned_patterns (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                pattern_type TEXT NOT NULL,
                pattern_text TEXT NOT NULL,
                score INTEGER NOT NULL,
                label TEXT,
                summary TEXT,
                evidence_source TEXT,
                confidence INTEGER,
                current_status TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS content_items (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                pillar TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS content_versions (
                id TEXT PRIMARY KEY,
                content_item_id TEXT NOT NULL,
                rewrite_job_id TEXT,
                version_label TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(content_item_id) REFERENCES content_items(id)
            );

            CREATE TABLE IF NOT EXISTS publish_records (
                id TEXT PRIMARY KEY,
                content_item_id TEXT NOT NULL,
                published_at TEXT NOT NULL,
                platform TEXT NOT NULL,
                metrics_json TEXT,
                FOREIGN KEY(content_item_id) REFERENCES content_items(id)
            );

            CREATE TABLE IF NOT EXISTS todo_items (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                source_module TEXT NOT NULL,
                source_report_id TEXT,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                action_type TEXT NOT NULL,
                suggested_due_label TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS douyin_oauth_sessions (
                state TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS douyin_authorizations (
                user_id TEXT PRIMARY KEY,
                open_id TEXT,
                access_token_encrypted TEXT,
                refresh_token_encrypted TEXT,
                access_token_expires_at TEXT,
                refresh_token_expires_at TEXT,
                scope_list TEXT,
                authorized_at TEXT,
                last_refreshed_at TEXT,
                status TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );


            CREATE TABLE IF NOT EXISTS benchmark_accounts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                account_name TEXT NOT NULL,
                platform TEXT NOT NULL,
                account_url TEXT,
                niche_label TEXT,
                account_tier TEXT NOT NULL,
                similarity_reason TEXT,
                learnability_reason TEXT,
                positioning_summary TEXT,
                why_selected TEXT,
                notes TEXT,
                source_mode TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS benchmark_content_samples (
                id TEXT PRIMARY KEY,
                benchmark_account_id TEXT NOT NULL,
                title TEXT NOT NULL,
                sample_url TEXT,
                content_type TEXT,
                pillar_guess TEXT,
                hook_style TEXT,
                conversion_style TEXT,
                sample_heat_level TEXT NOT NULL,
                sample_notes TEXT,
                metrics_snapshot_text TEXT,
                publish_date_text TEXT,
                why_it_worked TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(benchmark_account_id) REFERENCES benchmark_accounts(id)
            );

            CREATE TABLE IF NOT EXISTS benchmark_playbooks (
                id TEXT PRIMARY KEY,
                benchmark_account_id TEXT NOT NULL,
                playbook_type TEXT NOT NULL,
                summary TEXT NOT NULL,
                evidence_source TEXT,
                confidence INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(benchmark_account_id) REFERENCES benchmark_accounts(id)
            );

            CREATE TABLE IF NOT EXISTS positioning_versions (
                positioning_version_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                job_id TEXT NOT NULL,
                report_title TEXT NOT NULL,
                preview_text TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 0,
                is_frozen INTEGER NOT NULL DEFAULT 0,
                frozen_at TEXT,
                supersedes_version_id TEXT,
                change_level TEXT NOT NULL DEFAULT 'minor',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS provider_credentials (
                id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                owner_type TEXT NOT NULL,
                provider_name TEXT NOT NULL,
                masked_key TEXT NOT NULL,
                encrypted_key TEXT NOT NULL,
                is_active INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )

        _add_column_if_missing(conn, "account_audit_jobs", "user_id", "user_id TEXT")
        _add_column_if_missing(conn, "audit_reports", "user_id", "user_id TEXT")
        _add_column_if_missing(conn, "niche_map_reports", "user_id", "user_id TEXT")
        _add_column_if_missing(conn, "rewrite_engine_reports", "user_id", "user_id TEXT")
        _add_column_if_missing(conn, "content_iterations", "status", "status TEXT DEFAULT 'adopted'")
        _add_column_if_missing(conn, "learned_patterns", "label", "label TEXT")
        _add_column_if_missing(conn, "learned_patterns", "summary", "summary TEXT")
        _add_column_if_missing(conn, "learned_patterns", "evidence_source", "evidence_source TEXT")
        _add_column_if_missing(conn, "learned_patterns", "confidence", "confidence INTEGER")
        _add_column_if_missing(conn, "learned_patterns", "current_status", "current_status TEXT")
        _add_column_if_missing(conn, "learned_patterns", "updated_at", "updated_at TEXT")

        _add_column_if_missing(conn, "content_items", "title_or_working_title", "title_or_working_title TEXT")
        _add_column_if_missing(conn, "content_items", "content_goal", "content_goal TEXT DEFAULT '转咨询'")
        _add_column_if_missing(conn, "content_items", "source_plan_id", "source_plan_id TEXT")
        _add_column_if_missing(conn, "content_items", "source_positioning_id", "source_positioning_id TEXT")
        _add_column_if_missing(conn, "content_items", "chosen_version_id", "chosen_version_id TEXT")
        _add_column_if_missing(conn, "content_items", "latest_publish_record_id", "latest_publish_record_id TEXT")
        _add_column_if_missing(conn, "content_items", "latest_review_id", "latest_review_id TEXT")

        _add_column_if_missing(conn, "content_versions", "title", "title TEXT")
        _add_column_if_missing(conn, "content_versions", "cover_text", "cover_text TEXT")
        _add_column_if_missing(conn, "content_versions", "hook", "hook TEXT")
        _add_column_if_missing(conn, "content_versions", "body_script", "body_script TEXT")
        _add_column_if_missing(conn, "content_versions", "closing_cta", "closing_cta TEXT")
        _add_column_if_missing(conn, "content_versions", "comment_guide", "comment_guide TEXT")
        _add_column_if_missing(conn, "content_versions", "risk_notes", "risk_notes TEXT")
        _add_column_if_missing(conn, "content_versions", "is_adopted", "is_adopted INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "content_versions", "updated_at", "updated_at TEXT")

        _add_column_if_missing(conn, "publish_records", "version_id", "version_id TEXT")
        _add_column_if_missing(conn, "publish_records", "views", "views INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "likes", "likes INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "comments", "comments INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "favorites", "favorites INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "shares", "shares INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "profile_visits", "profile_visits INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "dm_count", "dm_count INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "inquiry_count", "inquiry_count INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "conversion_count", "conversion_count INTEGER DEFAULT 0")
        _add_column_if_missing(conn, "publish_records", "manual_notes", "manual_notes TEXT")
        _add_column_if_missing(conn, "publish_records", "created_at", "created_at TEXT")
        _add_column_if_missing(conn, "publish_records", "updated_at", "updated_at TEXT")

        _add_column_if_missing(conn, "review_entries", "content_item_id", "content_item_id TEXT")
        _add_column_if_missing(conn, "review_entries", "publish_record_id", "publish_record_id TEXT")
        _add_column_if_missing(conn, "review_entries", "version_id", "version_id TEXT")

        conn.execute(
            """
            UPDATE account_audit_jobs
            SET user_id = (
                SELECT user_id FROM accounts a WHERE a.id = account_audit_jobs.account_id
            )
            WHERE user_id IS NULL
            """
        )
        conn.execute(
            """
            UPDATE audit_reports
            SET user_id = (
                SELECT j.user_id FROM account_audit_jobs j WHERE j.id = audit_reports.job_id
            )
            WHERE user_id IS NULL
            """
        )
        conn.execute(
            """
            UPDATE niche_map_reports
            SET user_id = (
                SELECT j.user_id FROM niche_map_jobs j WHERE j.id = niche_map_reports.job_id
            )
            WHERE user_id IS NULL
            """
        )
        conn.execute(
            """
            UPDATE rewrite_engine_reports
            SET user_id = (
                SELECT j.user_id FROM rewrite_engine_jobs j WHERE j.id = rewrite_engine_reports.job_id
            )
            WHERE user_id IS NULL
            """
        )

        conn.execute(
            """
            UPDATE content_items
            SET title_or_working_title = COALESCE(title_or_working_title, title),
                content_goal = COALESCE(content_goal, '转咨询'),
                updated_at = COALESCE(updated_at, created_at)
            """
        )
        conn.execute(
            """
            UPDATE publish_records
            SET created_at = COALESCE(created_at, published_at),
                updated_at = COALESCE(updated_at, published_at)
            """
        )
        conn.execute(
            """
            UPDATE content_versions
            SET title = COALESCE(title, version_label),
                cover_text = COALESCE(cover_text, ''),
                hook = COALESCE(hook, ''),
                body_script = COALESCE(body_script, payload_json),
                closing_cta = COALESCE(closing_cta, ''),
                comment_guide = COALESCE(comment_guide, ''),
                risk_notes = COALESCE(risk_notes, ''),
                updated_at = COALESCE(updated_at, created_at),
                is_adopted = COALESCE(is_adopted, 0)
            """
        )

        conn.execute(
            """
            UPDATE learned_patterns
            SET label = COALESCE(label, pattern_text),
                summary = COALESCE(summary, pattern_text),
                evidence_source = COALESCE(evidence_source, 'review_lab'),
                confidence = COALESCE(confidence, score),
                current_status = COALESCE(current_status, 'candidate'),
                updated_at = COALESCE(updated_at, created_at)
            """
        )


if __name__ == "__main__":
    init_db()
    print(f"initialized: {DB_PATH}")
