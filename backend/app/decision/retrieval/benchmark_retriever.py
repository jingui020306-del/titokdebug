from __future__ import annotations

from app.decision.retrieval.embedding_service import embedding_service
from app.decision.retrieval.faiss_index import faiss_index
from app.decision.snapshot.schemas import BenchmarkAccountSnapshot


class BenchmarkRetriever:
    def retrieve(self, accounts: list[BenchmarkAccountSnapshot], query: str, top_k: int = 5) -> list[BenchmarkAccountSnapshot]:
        if not accounts:
            return []
        vectors = [embedding_service.encode(f"{x.account_name} {x.similarity_reason} {x.learnability_reason}") for x in accounts]
        qv = embedding_service.encode(query)
        idx = faiss_index.search(vectors, qv, top_k=top_k)
        return [accounts[i] for i in idx]


benchmark_retriever = BenchmarkRetriever()
