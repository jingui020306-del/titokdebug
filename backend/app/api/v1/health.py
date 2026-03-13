from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "creator-os-backend",
        "timestamp": datetime.utcnow().isoformat(),
    }
