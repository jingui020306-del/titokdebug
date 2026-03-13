from __future__ import annotations

import importlib
import importlib.util


class EmbeddingService:
    def __init__(self) -> None:
        self._available = importlib.util.find_spec("sentence_transformers") is not None
        self._model = None

    @property
    def available(self) -> bool:
        return self._available

    def encode(self, text: str) -> list[float]:
        if not self._available:
            return [float(len(text) % 13), float(text.count("咨询")), float(text.count("承接"))]
        if self._model is None:
            st = importlib.import_module("sentence_transformers")
            self._model = st.SentenceTransformer("all-MiniLM-L6-v2")
        vec = self._model.encode(text)
        return [float(x) for x in vec[:64]]


embedding_service = EmbeddingService()
