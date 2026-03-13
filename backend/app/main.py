from fastapi import FastAPI, Request

from app.api.v1 import api_v1_router
from app.core.config import get_settings
from app.core.db import init_db

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.include_router(api_v1_router)


@app.middleware("http")
async def dev_user_middleware(request: Request, call_next):
    """TODO: replace with real session/auth middleware."""
    request.state.user_id = request.headers.get("x-user-id", "dev-user")
    return await call_next(request)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
