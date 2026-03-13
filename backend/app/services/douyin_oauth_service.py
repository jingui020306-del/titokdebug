from __future__ import annotations

import base64
import json
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from app.core.config import get_settings
from app.core.db import get_conn
from app.schemas.douyin_oauth import DouyinOAuthStatus


def _encrypt(text: str) -> str:
    # TODO: replace with KMS/managed envelope encryption.
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


class DouyinOAuthService:
    def start(self, user_id: str) -> dict[str, str | bool]:
        settings = get_settings()
        state = secrets.token_urlsafe(24)
        now = datetime.now(timezone.utc)
        with get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO douyin_oauth_sessions (state, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
                (state, user_id, now.isoformat(), (now + timedelta(minutes=15)).isoformat()),
            )

        configured = bool(settings.douyin_client_key and settings.douyin_client_secret and settings.douyin_redirect_uri)
        scopes = "user_info,video_data.read"
        auth_url = (
            "https://open.douyin.com/platform/oauth/connect/?"
            + urlencode(
                {
                    "client_key": settings.douyin_client_key or "DEV_MISSING_CLIENT_KEY",
                    "redirect_uri": settings.douyin_redirect_uri or "http://localhost:8000/api/v1/douyin/oauth/callback",
                    "response_type": "code",
                    "scope": scopes,
                    "state": state,
                }
            )
        )
        return {
            "authorize_url": auth_url,
            "state": state,
            "configured": configured,
            "message": "已生成官方 OAuth 授权链接。" if configured else "当前未配置抖音开放平台凭证，将进入开发 fallback 模式。",
        }

    def callback(self, user_id: str, code: str | None, state: str | None) -> dict[str, str | bool]:
        if not code or not state:
            return {"ok": False, "message": "缺少 code 或 state。"}

        with get_conn() as conn:
            row = conn.execute("SELECT * FROM douyin_oauth_sessions WHERE state = ? AND user_id = ?", (state, user_id)).fetchone()
        if not row:
            return {"ok": False, "message": "state 无效或已过期。"}

        settings = get_settings()
        configured = bool(settings.douyin_client_key and settings.douyin_client_secret and settings.douyin_redirect_uri)
        now = datetime.now(timezone.utc)

        if not configured:
            with get_conn() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO douyin_authorizations
                    (user_id, open_id, access_token_encrypted, refresh_token_encrypted, access_token_expires_at, refresh_token_expires_at, scope_list, authorized_at, last_refreshed_at, status, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        f"mock_open_id_{user_id}",
                        _encrypt("mock_access_token"),
                        _encrypt("mock_refresh_token"),
                        (now + timedelta(hours=4)).isoformat(),
                        (now + timedelta(days=30)).isoformat(),
                        json.dumps(["user_info", "video_data.read"], ensure_ascii=False),
                        now.isoformat(),
                        now.isoformat(),
                        "connected",
                        now.isoformat(),
                    ),
                )
            return {"ok": True, "fallback_mode": True, "message": "开发环境 fallback 授权成功（未走真实 token 交换）。"}

        # TODO: call real Douyin token exchange endpoint with code/client_key/client_secret.
        with get_conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO douyin_authorizations
                (user_id, open_id, access_token_encrypted, refresh_token_encrypted, access_token_expires_at, refresh_token_expires_at, scope_list, authorized_at, last_refreshed_at, status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    "TODO_OPEN_ID",
                    _encrypt("TODO_REAL_ACCESS_TOKEN"),
                    _encrypt("TODO_REAL_REFRESH_TOKEN"),
                    (now + timedelta(hours=4)).isoformat(),
                    (now + timedelta(days=30)).isoformat(),
                    json.dumps(["user_info", "video_data.read"], ensure_ascii=False),
                    now.isoformat(),
                    now.isoformat(),
                    "connected",
                    now.isoformat(),
                ),
            )
        return {"ok": True, "fallback_mode": False, "message": "OAuth 骨架流程已完成，等待接入真实 token 交换。"}

    def refresh(self, user_id: str) -> dict[str, str]:
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM douyin_authorizations WHERE user_id = ?", (user_id,)).fetchone()
        if not row:
            return {"status": "need_reauthorize", "message": "未连接账号，请先授权。"}

        if row["status"] == "disconnected":
            return {"status": "need_reauthorize", "message": "授权已断开，请重新授权。"}

        # TODO: real refresh_token exchange.
        now = datetime.now(timezone.utc)
        with get_conn() as conn:
            conn.execute(
                "UPDATE douyin_authorizations SET access_token_expires_at = ?, last_refreshed_at = ?, updated_at = ?, status = ? WHERE user_id = ?",
                ((now + timedelta(hours=4)).isoformat(), now.isoformat(), now.isoformat(), "connected", user_id),
            )
        return {"status": "ok", "message": "已刷新 access token（骨架逻辑）。"}

    def disconnect(self, user_id: str) -> dict[str, str]:
        now = datetime.now(timezone.utc).isoformat()
        with get_conn() as conn:
            conn.execute(
                "UPDATE douyin_authorizations SET status = ?, updated_at = ? WHERE user_id = ?",
                ("disconnected", now, user_id),
            )
        return {"status": "ok", "message": "已断开抖音授权。"}

    def status(self, user_id: str) -> DouyinOAuthStatus:
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM douyin_authorizations WHERE user_id = ?", (user_id,)).fetchone()
        if not row:
            return DouyinOAuthStatus(status="未连接", fallback_mode=True, message="未检测到授权记录。")

        if row["status"] == "disconnected":
            return DouyinOAuthStatus(status="需要重新授权", fallback_mode=True, message="授权已断开。")

        expires_at = datetime.fromisoformat(row["access_token_expires_at"])
        now = datetime.now(timezone.utc)
        if expires_at < now:
            st = "需要重新授权"
        elif expires_at - now < timedelta(minutes=30):
            st = "access_token即将过期"
        else:
            st = "已连接"

        return DouyinOAuthStatus(
            status=st,
            fallback_mode=bool(str(row["open_id"]).startswith("mock_open_id")),
            authorized_at=datetime.fromisoformat(row["authorized_at"]) if row["authorized_at"] else None,
            scope_list=json.loads(row["scope_list"] or "[]"),
            message="授权状态正常" if st == "已连接" else "建议刷新或重新授权",
        )


douyin_oauth_service = DouyinOAuthService()
