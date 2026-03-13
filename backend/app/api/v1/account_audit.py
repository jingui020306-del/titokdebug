from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.api.deps.auth import auth_guard
from app.schemas.account_audit import (
    AccountAuditHistoryResponse,
    AccountAuditJobStatusResponse,
    AccountAuditReportsResponse,
    DeepReportResponse,
    FastReportResponse,
    MockCreateRequest,
    MockCreateResponse,
    SupplementRequest,
)
from app.services.account_audit_service import account_audit_service

router = APIRouter(prefix="/account-audit", tags=["account-audit"])


@router.post("/mock-create", response_model=MockCreateResponse)
def mock_create(payload: MockCreateRequest, user_id: str = Depends(auth_guard)) -> MockCreateResponse:
    job_id = account_audit_service.create_mock_job(user_id=user_id, payload=payload)
    return MockCreateResponse(job_id=job_id, status="created", message="Mock 任务创建成功")


@router.get("/history", response_model=AccountAuditHistoryResponse)
def get_history(user_id: str = Depends(auth_guard)) -> AccountAuditHistoryResponse:
    return AccountAuditHistoryResponse(items=account_audit_service.get_history(user_id=user_id))


@router.get("/{job_id}/status", response_model=AccountAuditJobStatusResponse)
def get_status(job_id: str, user_id: str = Depends(auth_guard)) -> AccountAuditJobStatusResponse:
    try:
        item = account_audit_service.get_job(user_id, job_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"job_id not found: {job_id}") from exc
    return AccountAuditJobStatusResponse(data=item)


@router.get("/{job_id}/reports", response_model=AccountAuditReportsResponse)
def get_reports(job_id: str, user_id: str = Depends(auth_guard)) -> AccountAuditReportsResponse:
    return AccountAuditReportsResponse(job_id=job_id, reports=account_audit_service.list_reports(user_id, job_id))


@router.get("/{job_id}/export-json")
def export_json(job_id: str, user_id: str = Depends(auth_guard)):
    try:
        payload = account_audit_service.export_report_json(user_id, job_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"job_id not found or no report: {job_id}") from exc
    return JSONResponse(content=payload)


@router.post("/{job_id}/rerun")
def rerun(job_id: str, user_id: str = Depends(auth_guard)) -> dict[str, str]:
    account_audit_service.get_job(user_id, job_id)
    account_audit_service.rerun(job_id)
    return {"status": "rerun_triggered"}


@router.post("/{job_id}/supplement", response_model=DeepReportResponse)
def supplement(job_id: str, payload: SupplementRequest, user_id: str = Depends(auth_guard)) -> DeepReportResponse:
    account_audit_service.add_supplement(user_id, job_id, payload)
    report = account_audit_service.get_report(user_id, job_id, "deep")
    if not report:
        return DeepReportResponse(status="loading", message="深度报告生成中", data=None)
    return DeepReportResponse(status="ready", message="报告生成成功", data=report)


@router.get("/{job_id}/fast-report", response_model=FastReportResponse)
def fast_report(job_id: str, user_id: str = Depends(auth_guard)) -> FastReportResponse:
    report = account_audit_service.get_report(user_id, job_id, "fast")
    if not report:
        return FastReportResponse(status="loading", message="快速报告生成中", data=None)
    return FastReportResponse(status="ready", message="报告生成成功", data=report)


@router.get("/{job_id}/deep-report", response_model=DeepReportResponse)
def deep_report(job_id: str, user_id: str = Depends(auth_guard)) -> DeepReportResponse:
    report = account_audit_service.get_report(user_id, job_id, "deep")
    if not report:
        return DeepReportResponse(status="loading", message="深度报告生成中", data=None)
    return DeepReportResponse(status="ready", message="报告生成成功", data=report)
