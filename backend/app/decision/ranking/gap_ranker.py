from __future__ import annotations

import importlib.util
from pathlib import Path

from app.decision.ranking.features.gap_features import gap_feature_vector
from app.decision.snapshot.schemas import UserGrowthSnapshot


class GapRanker:
    def __init__(self) -> None:
        self.artifact_path = Path(__file__).resolve().parent / "artifacts" / "gap_ranker.model"
        self.model_available = self.artifact_path.exists() and importlib.util.find_spec("lightgbm") is not None

    def score(self, dimension: str, snapshot: UserGrowthSnapshot) -> float:
        feats = gap_feature_vector(dimension, snapshot)
        if not self.model_available:
            return feats["dimension_bias"] + (1 - feats["inquiry_signal"]) + (1 - feats["conversion_signal"]) + (1 - feats["positioning_frozen_signal"]) / 2
        return feats["dimension_bias"]


gap_ranker = GapRanker()
