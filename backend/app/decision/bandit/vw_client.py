from __future__ import annotations

import importlib.util


class VwClient:
    def __init__(self) -> None:
        self.available = importlib.util.find_spec("vowpalwabbit") is not None

    def choose(self, scored_candidates: list[tuple[dict[str, str], float]]) -> dict[str, str]:
        if not scored_candidates:
            return {}
        # Phase-1 fallback: if VW unavailable (or not configured), return top scored candidate.
        return sorted(scored_candidates, key=lambda x: x[1], reverse=True)[0][0]


vw_client = VwClient()
