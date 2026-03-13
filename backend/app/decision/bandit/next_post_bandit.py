from __future__ import annotations

from app.decision.bandit.vw_client import vw_client


class NextPostBandit:
    def choose(self, scored_candidates: list[tuple[dict[str, str], float]]) -> dict[str, str]:
        return vw_client.choose(scored_candidates)


next_post_bandit = NextPostBandit()
