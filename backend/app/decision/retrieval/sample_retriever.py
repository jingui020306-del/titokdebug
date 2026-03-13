from __future__ import annotations

from app.decision.snapshot.schemas import BenchmarkContentSampleSnapshot


class SampleRetriever:
    def retrieve(self, samples: list[BenchmarkContentSampleSnapshot], benchmark_ids: list[str], top_k: int = 10) -> list[BenchmarkContentSampleSnapshot]:
        filtered = [x for x in samples if x.benchmark_account_id in set(benchmark_ids)]
        return filtered[:top_k]


sample_retriever = SampleRetriever()
