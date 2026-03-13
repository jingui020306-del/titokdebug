from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AccountSnapshot:
    id: str
    account_id: str
    job_id: str
    followers: int
    following: int
    bio: str
    category: str
    city: str
    captured_at: datetime
