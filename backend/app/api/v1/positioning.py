from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.auth import auth_guard
from app.schemas.account_audit import DeepReportResponse, FastReportResponse, MockCreateRequest, MockCreateResponse
from app.schemas.common import ApiResponse, PositioningVersionSummary
from app.services.account_audit_service import account_audit_service
from app.services.positioning_service import positioning_service

router = APIRouter(prefix="/positioning", tags=["positioning"])


@router.post("/mock-create", response_model=MockCreateResponse)
def create_positioning(payload: MockCreateRequest, user_id: str = Depends(auth_guard)) -> MockCreateResponse:
    job_id = account_audit_service.create_mock_job(user_id=user_id, payload=payload)
    return MockCreateResponse(job_id=job_id, status="created", message="定位任务创建成功")


@router.get("/{job_id}/report", response_model=DeepReportResponse)
def get_positioning_report(job_id: str, user_id: str = Depends(auth_guard)) -> DeepReportResponse:
    report = account_audit_service.get_report(user_id, job_id, "deep")
    if not report:
        report = account_audit_service.get_report(user_id, job_id, "fast")
        if report:
            positioning_service.ensure_version_from_job(user_id, job_id)
            return FastReportResponse(status="ready", message="使用快速版定位报告", data=report)
        return DeepReportResponse(status="loading", message="定位报告生成中", data=None)
    positioning_service.ensure_version_from_job(user_id, job_id)
    return DeepReportResponse(status="ready", message="定位报告生成成功", data=report)


@router.get("/history", response_model=ApiResponse[list[PositioningVersionSummary]])
def get_positioning_history(user_id: str = Depends(auth_guard)) -> ApiResponse[list[PositioningVersionSummary]]:
    return ApiResponse(success=True, data=positioning_service.list_versions(user_id))


@router.post("/{job_id}/freeze", response_model=ApiResponse[dict[str, str]])
def freeze_positioning(job_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[dict[str, str]]:
    if not positioning_service.freeze(user_id, job_id):
        raise HTTPException(status_code=404, detail="positioning version not found")
    return ApiResponse(success=True, data={"job_id": job_id, "status": "frozen"})


@router.post("/{job_id}/set-active", response_model=ApiResponse[dict[str, str]])
def set_active_positioning(job_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[dict[str, str]]:
    if not positioning_service.set_active(user_id, job_id):
        raise HTTPException(status_code=404, detail="positioning version not found")
    return ApiResponse(success=True, data={"job_id": job_id, "status": "active"})


@router.get("/active", response_model=ApiResponse[PositioningVersionSummary])
def get_active_positioning(user_id: str = Depends(auth_guard)) -> ApiResponse[PositioningVersionSummary]:
    active = positioning_service.get_active(user_id)
    if not active:
        raise HTTPException(status_code=404, detail="active positioning not found")
    return ApiResponse(success=True, data=active)
