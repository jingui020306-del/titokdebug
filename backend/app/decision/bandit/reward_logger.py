from __future__ import annotations

from datetime import datetime, timezone


class RewardLogger:
    def log(self, *, user_id: str, content_item_id: str, views: int, favorites: int, profile_visits: int, dm_count: int, inquiry_count: int, conversion_count: int) -> dict[str, str | int]:
        # Phase-1: structured stub for future persistence to event store.
        return {
            "user_id": user_id,
            "content_item_id": content_item_id,
            "views": views,
            "favorites": favorites,
            "profile_visits": profile_visits,
            "dm_count": dm_count,
            "inquiry_count": inquiry_count,
            "conversion_count": conversion_count,
            "logged_at": datetime.now(timezone.utc).isoformat(),
        }


reward_logger = RewardLogger()
