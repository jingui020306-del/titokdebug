from __future__ import annotations

import importlib.util
from pathlib import Path

from app.decision.ranking.features.benchmark_features import benchmark_feature_vector
from app.decision.snapshot.schemas import BenchmarkAccountSnapshot, UserGrowthSnapshot


class BenchmarkRanker:
    def __init__(self) -> None:
        self.artifact_path = Path(__file__).resolve().parent / "artifacts" / "benchmark_ranker.model"
        self.model_available = self.artifact_path.exists() and importlib.util.find_spec("lightgbm") is not None

    def score(self, account: BenchmarkAccountSnapshot, snapshot: UserGrowthSnapshot) -> float:
        feats = benchmark_feature_vector(account, snapshot)
        if not self.model_available:
            return sum(feats.values())
        # placeholder for future model loading
        return sum(feats.values())


benchmark_ranker = BenchmarkRanker()
