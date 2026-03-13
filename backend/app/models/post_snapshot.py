from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PostSnapshotModel:
    id: str
    job_id: str
    post_id: str
    title: str
    topic: str
    views: int
    likes: int
    comments: int
    shares: int
    publish_time: datetime
