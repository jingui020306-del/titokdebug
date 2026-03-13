from __future__ import annotations

from datetime import datetime
from typing import Literal

from app.schemas.common import ReportPreviewMixin

from pydantic import BaseModel, Field


class RewriteInput(BaseModel):
    platform: Literal["抖音", "小红书"]
    goal: Literal["涨粉", "收藏", "评论", "私信", "主页访问", "转咨询"]
    original_title: str
    original_script: str
    original_cover_text: str
    current_issues: list[Literal["没播放", "有播放不涨粉", "有播放不转化", "标题太平", "前3秒弱", "结尾无引导"]] = Field(default_factory=list)
    style_limits: list[Literal["避免敏感承诺", "避免强营销", "不能太口语化", "不能太像 AI"]] = Field(default_factory=list)
    industry: str
    target_audience: str


class RewriteVariant(BaseModel):
    label: str
    content: str
    rationale: str


class RewriteReport(ReportPreviewMixin):
    job_id: str
    created_at: datetime
    rewrite_input: RewriteInput
    diagnosis_summary: str
    title_variants: list[RewriteVariant]
    cover_variants: list[RewriteVariant]
    hook_variants: list[RewriteVariant]
    body_script: str
    closing_cta: str
    comment_guide: str
    risk_replacements: list[dict[str, str]]
    recommended_use_case: dict[str, str]


class RewriteCreateResponse(BaseModel):
    job_id: str
    status: str
    message: str


class RewriteHistoryItem(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    platform: str
    goal: str


class RewriteHistoryResponse(BaseModel):
    items: list[RewriteHistoryItem]


class RewriteReportResponse(BaseModel):
    status: Literal["ready", "loading", "error"]
    data: RewriteReport | None
