from fastapi import APIRouter, Depends

from app.api.deps.auth import auth_guard
from app.schemas.common import ApiResponse
from app.services.frontstage_service import frontstage_service

router = APIRouter(tags=["frontstage"])


@router.get("/home/summary", response_model=ApiResponse[dict])
def get_home_summary(user_id: str = Depends(auth_guard)) -> ApiResponse[dict]:
    return ApiResponse(success=True, data=frontstage_service.home_summary(user_id))


@router.get("/my-account/summary", response_model=ApiResponse[dict])
def get_my_account_summary(user_id: str = Depends(auth_guard)) -> ApiResponse[dict]:
    return ApiResponse(success=True, data=frontstage_service.my_account_summary(user_id))


@router.get("/learn-from/summary", response_model=ApiResponse[dict])
def get_learn_from_summary(user_id: str = Depends(auth_guard)) -> ApiResponse[dict]:
    return ApiResponse(success=True, data=frontstage_service.learn_from_summary(user_id))


@router.get("/upgrade-plan/summary", response_model=ApiResponse[dict])
def get_upgrade_plan_summary(user_id: str = Depends(auth_guard)) -> ApiResponse[dict]:
    return ApiResponse(success=True, data=frontstage_service.upgrade_plan_summary(user_id))


@router.get("/execute/summary", response_model=ApiResponse[dict])
def get_execute_summary(user_id: str = Depends(auth_guard)) -> ApiResponse[dict]:
    return ApiResponse(success=True, data=frontstage_service.execute_summary(user_id))


@router.get("/review/summary", response_model=ApiResponse[dict])
def get_review_summary(user_id: str = Depends(auth_guard)) -> ApiResponse[dict]:
    return ApiResponse(success=True, data=frontstage_service.review_summary(user_id))
