from __future__ import annotations

from app.decision.snapshot.schemas import UserGrowthSnapshot


def gap_feature_vector(dimension: str, snapshot: UserGrowthSnapshot) -> dict[str, float]:
    inquiry = sum(x.inquiry_count for x in snapshot.publish_records)
    conversion = sum(x.conversion_count for x in snapshot.publish_records)
    return {
        "dimension_bias": 1.0 if dimension in {"主页承接", "咨询承接方式"} else 0.6,
        "inquiry_signal": 0.2 if inquiry == 0 else 0.7,
        "conversion_signal": 0.2 if conversion == 0 else 0.8,
        "positioning_frozen_signal": 1.0 if snapshot.frozen_positioning else 0.4,
    }
