from __future__ import annotations

from app.decision.snapshot.schemas import UserGrowthSnapshot


def next_post_feature_vector(candidate: dict[str, str], snapshot: UserGrowthSnapshot, top_gap: str) -> dict[str, float]:
    is_consult = 1.0 if candidate.get("goal") == "咨询" else 0.6
    gap_match = 1.0 if top_gap in {"主页承接", "咨询承接方式"} and is_consult == 1.0 else 0.7
    return {
        "gap_match": gap_match,
        "consultation_fit": is_consult,
        "stage_fit": 0.8 if snapshot.active_positioning.has_active else 0.5,
        "risk_penalty": 0.2 if "泛" in candidate.get("topic", "") else 0.05,
    }
