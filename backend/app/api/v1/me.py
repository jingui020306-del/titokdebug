from fastapi import APIRouter, Depends

from app.api.deps.auth import CurrentUser, current_user
from app.schemas.user import MeOverview, UserProfile
from app.services.user_service import user_service

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=UserProfile)
def get_me(user: CurrentUser = Depends(current_user)) -> UserProfile:
    return user_service.ensure_user(user.id, user.name, user.email)


@router.get("/overview", response_model=MeOverview)
def get_me_overview(user: CurrentUser = Depends(current_user)) -> MeOverview:
    user_service.ensure_user(user.id, user.name, user.email)
    return user_service.get_overview(user.id)
