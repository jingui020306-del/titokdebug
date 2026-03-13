from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

JobSourceType = Literal["mock", "oauth"]
JobStatus = Literal["created", "syncing_fast", "fast_ready", "syncing_deep", "deep_ready", "failed"]


@dataclass
class AccountAuditJob:
    id: str
    account_id: str
    source_type: JobSourceType
    status: JobStatus
    report_mode_available: str
    created_at: datetime
    updated_at: datetime
    error_message: str | None = None
