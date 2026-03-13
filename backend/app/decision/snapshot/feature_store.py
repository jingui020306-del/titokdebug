from __future__ import annotations

from dataclasses import dataclass

from app.decision.snapshot.schemas import UserGrowthSnapshot


@dataclass
class SnapshotFeatureStore:
    snapshot: UserGrowthSnapshot

    @property
    def validated_pattern_count(self) -> int:
        return len([x for x in self.snapshot.learned_patterns if x.current_status == "validated"])

    @property
    def benchmark_pool_size(self) -> int:
        return len(self.snapshot.benchmark_accounts)

    @property
    def published_count(self) -> int:
        return len(self.snapshot.publish_records)

    @property
    def total_inquiries(self) -> int:
        return sum(x.inquiry_count for x in self.snapshot.publish_records)

    @property
    def unreviewed_published_count(self) -> int:
        review_ids = {r.id for r in self.snapshot.recent_reviews}
        # Lightweight heuristic: if there are publish records and too few reviews, assume pending review.
        return max(0, len(self.snapshot.publish_records) - len(review_ids))
