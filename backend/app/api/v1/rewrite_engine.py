from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.auth import auth_guard
from app.schemas.rewrite_engine import RewriteCreateResponse, RewriteHistoryResponse, RewriteInput, RewriteReportResponse
from app.services.rewrite_engine_service import rewrite_engine_service

router = APIRouter(prefix="/rewrite-engine", tags=["rewrite-engine"])


@router.post("/mock-create", response_model=RewriteCreateResponse)
def mock_create(payload: RewriteInput, user_id: str = Depends(auth_guard)) -> RewriteCreateResponse:
    job_id = rewrite_engine_service.create_mock(user_id=user_id, payload=payload)
    return RewriteCreateResponse(job_id=job_id, status="created", message="改稿任务已创建")


@router.get("/{job_id}/report", response_model=RewriteReportResponse)
def get_report(job_id: str, user_id: str = Depends(auth_guard)) -> RewriteReportResponse:
    report = rewrite_engine_service.get_report(job_id, user_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"job_id not found: {job_id}")
    return RewriteReportResponse(status="ready", data=report)


@router.get("/history", response_model=RewriteHistoryResponse)
def get_history(user_id: str = Depends(auth_guard)) -> RewriteHistoryResponse:
    return RewriteHistoryResponse(items=rewrite_engine_service.get_history(user_id=user_id))
