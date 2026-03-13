from __future__ import annotations

from app.decision.snapshot.schemas import BenchmarkAccountSnapshot, UserGrowthSnapshot


def benchmark_feature_vector(account: BenchmarkAccountSnapshot, snapshot: UserGrowthSnapshot) -> dict[str, float]:
    text = f"{account.similarity_reason} {account.learnability_reason} {account.why_selected}"
    return {
        "similarity_score": 0.8 if "同" in text else 0.5,
        "goal_match_score": 0.9 if "咨询" in text else 0.6,
        "learnability_score": 0.9 if account.account_tier in {"mid", "peer"} else 0.6,
        "benchmark_strength_score": 0.8 if account.account_tier in {"head", "mid"} else 0.6,
        "sample_coverage_score": min(1.0, len([s for s in snapshot.benchmark_samples if s.benchmark_account_id == account.id]) / 3),
    }
