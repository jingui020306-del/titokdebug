from __future__ import annotations

import importlib
import importlib.util


class FaissIndex:
    def __init__(self) -> None:
        self._available = importlib.util.find_spec("faiss") is not None

    @property
    def available(self) -> bool:
        return self._available

    def search(self, vectors: list[list[float]], query: list[float], top_k: int = 5) -> list[int]:
        if not vectors:
            return []
        if not self._available:
            scored = sorted(range(len(vectors)), key=lambda i: abs(sum(vectors[i]) - sum(query)))
            return scored[:top_k]

        faiss = importlib.import_module("faiss")
        dim = len(query)
        index = faiss.IndexFlatL2(dim)
        import numpy as np

        mat = np.array(vectors, dtype="float32")
        q = np.array([query], dtype="float32")
        index.add(mat)
        _, idx = index.search(q, min(top_k, len(vectors)))
        return [int(x) for x in idx[0]]


faiss_index = FaissIndex()
