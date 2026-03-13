from fastapi import APIRouter, Depends

from app.api.deps.auth import auth_guard
from app.schemas.douyin_oauth import DouyinOAuthStatus
from app.services.douyin_oauth_service import douyin_oauth_service

router = APIRouter(prefix="/douyin/oauth", tags=["douyin-oauth"])


@router.get("/start")
def oauth_start(user_id: str = Depends(auth_guard)) -> dict[str, str | bool]:
    return douyin_oauth_service.start(user_id)


@router.get("/callback")
def oauth_callback(code: str | None = None, state: str | None = None, user_id: str = Depends(auth_guard)) -> dict[str, str | bool]:
    return douyin_oauth_service.callback(user_id=user_id, code=code, state=state)


@router.post("/refresh")
def oauth_refresh(user_id: str = Depends(auth_guard)) -> dict[str, str]:
    return douyin_oauth_service.refresh(user_id)


@router.post("/disconnect")
def oauth_disconnect(user_id: str = Depends(auth_guard)) -> dict[str, str]:
    return douyin_oauth_service.disconnect(user_id)


@router.get("/status", response_model=DouyinOAuthStatus)
def oauth_status(user_id: str = Depends(auth_guard)) -> DouyinOAuthStatus:
    return douyin_oauth_service.status(user_id)
