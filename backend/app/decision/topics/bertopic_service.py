from __future__ import annotations

import importlib.util

from app.decision.topics.topic_taxonomy import CONTENT_TYPE_TAXONOMY


class BERTopicService:
    def __init__(self) -> None:
        self.available = importlib.util.find_spec("bertopic") is not None

    def fit(self, docs: list[str]) -> dict[str, int]:
        if not docs:
            return {}
        # phase-1 fallback summary
        return {self.fallback_label(doc): 1 for doc in docs[:20]}

    def predict(self, doc: str) -> str:
        if not doc:
            return "观点型"
        return self.fallback_label(doc)

    def fallback_label(self, doc: str) -> str:
        if "案例" in doc:
            return "案例型"
        if "咨询" in doc or "私信" in doc:
            return "咨询承接型"
        if "对比" in doc:
            return "对比型"
        if "流程" in doc or "步骤" in doc:
            return "流程型"
        return CONTENT_TYPE_TAXONOMY[0]


bertopic_service = BERTopicService()
