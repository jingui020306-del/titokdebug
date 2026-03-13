from fastapi import APIRouter

from app.api.v1.account_audit import router as account_audit_router
from app.api.v1.content_studio import router as content_studio_router
from app.api.v1.dev import router as dev_router
from app.api.v1.douyin_oauth import router as douyin_oauth_router
from app.api.v1.frontstage import router as frontstage_router
from app.api.v1.health import router as health_router
from app.api.v1.me import router as me_router
from app.api.v1.niche_map import router as niche_map_router
from app.api.v1.positioning import router as positioning_router
from app.api.v1.review_lab import router as review_lab_router
from app.api.v1.rewrite_engine import router as rewrite_engine_router
from app.api.v1.settings import router as settings_router
from app.api.v1.workspace import router as workspace_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health_router)
api_v1_router.include_router(me_router)
api_v1_router.include_router(douyin_oauth_router)
api_v1_router.include_router(workspace_router)
api_v1_router.include_router(frontstage_router)
api_v1_router.include_router(positioning_router)
api_v1_router.include_router(content_studio_router)
api_v1_router.include_router(review_lab_router)

# Backward-compatible legacy routes.
api_v1_router.include_router(account_audit_router)
api_v1_router.include_router(niche_map_router)
api_v1_router.include_router(rewrite_engine_router)
api_v1_router.include_router(dev_router)
api_v1_router.include_router(settings_router)
