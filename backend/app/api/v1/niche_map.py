from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.auth import auth_guard
from app.schemas.niche_map import NicheInput, NicheMapCreateResponse, NicheMapHistoryResponse, NicheMapReportResponse
from app.services.niche_map_service import niche_map_service

router = APIRouter(prefix="/niche-map", tags=["niche-map"])


@router.post("/mock-create", response_model=NicheMapCreateResponse)
def mock_create(payload: NicheInput, user_id: str = Depends(auth_guard)) -> NicheMapCreateResponse:
    job_id = niche_map_service.create_mock(user_id=user_id, payload=payload)
    return NicheMapCreateResponse(job_id=job_id, status="created", message="赛道地图任务已创建")


@router.get("/{job_id}/report", response_model=NicheMapReportResponse)
def get_report(job_id: str, user_id: str = Depends(auth_guard)) -> NicheMapReportResponse:
    report = niche_map_service.get_report(job_id, user_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"job_id not found: {job_id}")
    return NicheMapReportResponse(status="ready", data=report)


@router.get("/history", response_model=NicheMapHistoryResponse)
def get_history(user_id: str = Depends(auth_guard)) -> NicheMapHistoryResponse:
    return NicheMapHistoryResponse(items=niche_map_service.get_history(user_id=user_id))
