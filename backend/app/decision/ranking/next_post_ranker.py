from __future__ import annotations

import importlib.util
from pathlib import Path

from app.decision.ranking.features.next_post_features import next_post_feature_vector
from app.decision.snapshot.schemas import UserGrowthSnapshot


class NextPostRanker:
    def __init__(self) -> None:
        self.artifact_path = Path(__file__).resolve().parent / "artifacts" / "next_post_ranker.model"
        self.model_available = self.artifact_path.exists() and importlib.util.find_spec("lightgbm") is not None

    def score(self, candidate: dict[str, str], snapshot: UserGrowthSnapshot, top_gap: str) -> float:
        feats = next_post_feature_vector(candidate, snapshot, top_gap)
        if not self.model_available:
            return feats["gap_match"] + feats["consultation_fit"] + feats["stage_fit"] - feats["risk_penalty"]
        return feats["gap_match"]


next_post_ranker = NextPostRanker()
