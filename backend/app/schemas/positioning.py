from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class PositioningScore(BaseModel):
    name: Literal["定位清晰度", "主页承接力", "内容集中度", "咨询转化适配度", "风险暴露度"]
    score: int
    reason: str


class PositioningReport(BaseModel):
    job_id: str
    generated_at: datetime
    report_title: str
    preview_text: str
    recommended_next_module: Literal["content_studio", "review_lab", "positioning"]
    executive_summary: str
    one_line_positioning: str
    target_audience_summary: str
    profile_rewrite_suggestions: dict[str, str]
    content_pillars: list[dict[str, str]]
    off_limit_directions: list[str]
    current_positioning_problems: list[str]
    evidence_chain: list[str]
    next_best_action: str
    scorecard: list[PositioningScore]


class PositioningHistoryItem(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    nickname: str
