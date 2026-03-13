from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class DouyinOAuthStatus(BaseModel):
    status: Literal["未连接", "已连接", "access_token即将过期", "需要重新授权"]
    fallback_mode: bool
    authorized_at: datetime | None = None
    scope_list: list[str] = []
    message: str
