from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class AuditReport:
    id: str
    job_id: str
    report_type: Literal["account_audit"]
    mode: Literal["fast", "deep"]
    version: int
    payload_json: str
    created_at: datetime
