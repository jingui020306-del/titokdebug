from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Account:
    id: str
    user_id: str
    source_type: Literal["mock", "oauth"]
    external_id: str | None
    nickname: str
    created_at: datetime
    updated_at: datetime
