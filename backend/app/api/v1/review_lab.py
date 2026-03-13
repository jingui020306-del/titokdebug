from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps.auth import auth_guard
from app.schemas.common import ApiResponse
from app.schemas.review_lab import (
    AccountUpgradePlan,
    BenchmarkAccountSummary,
    BenchmarkContentSample,
    BenchmarkCreateRequest,
    BenchmarkGapSummary,
    BenchmarkPatchRequest,
    BenchmarkSampleCreateRequest,
    DiscoveryConfirmRequest,
    DiscoverySearchRequest,
    ReviewCreateRequest,
    ReviewHistoryItem,
    ReviewReport,
)
from app.services.benchmark_service import benchmark_service
from app.services.review_lab_service import review_lab_service

router = APIRouter(prefix="/review-lab", tags=["review-lab"])


@router.post("/new", response_model=ApiResponse[dict[str, str]])
def create_review(payload: ReviewCreateRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[dict[str, str]]:
    review_id = review_lab_service.create_review(user_id, payload)
    return ApiResponse(success=True, data={"review_id": review_id, "status": "created"})


@router.get("/report/{review_id}", response_model=ApiResponse[ReviewReport])
def get_review_report(review_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[ReviewReport]:
    report = review_lab_service.get_report(user_id, review_id)
    if not report:
        raise HTTPException(status_code=404, detail="review not found")
    return ApiResponse(success=True, data=report)


@router.get("/history", response_model=ApiResponse[list[ReviewHistoryItem]])
def review_history(
    pillar: str | None = Query(default=None, description="按内容支柱筛选"),
    user_id: str = Depends(auth_guard),
) -> ApiResponse[list[ReviewHistoryItem]]:
    return ApiResponse(success=True, data=review_lab_service.history(user_id, pillar=pillar))


@router.post("/discovery/search", response_model=ApiResponse[list])
def discovery_search(payload: DiscoverySearchRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[list]:
    return ApiResponse(success=True, data=benchmark_service.discovery_search(user_id, payload))


@router.post("/discovery/confirm", response_model=ApiResponse[list[BenchmarkAccountSummary]])
def discovery_confirm(payload: DiscoveryConfirmRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[list[BenchmarkAccountSummary]]:
    return ApiResponse(success=True, data=benchmark_service.confirm_candidates(user_id, payload.candidates))


@router.get("/benchmarks", response_model=ApiResponse[list[BenchmarkAccountSummary]])
def list_benchmarks(user_id: str = Depends(auth_guard)) -> ApiResponse[list[BenchmarkAccountSummary]]:
    return ApiResponse(success=True, data=benchmark_service.list_benchmarks(user_id))


@router.post("/benchmarks", response_model=ApiResponse[BenchmarkAccountSummary])
def create_benchmark(payload: BenchmarkCreateRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[BenchmarkAccountSummary]:
    return ApiResponse(success=True, data=benchmark_service.create_benchmark(user_id, payload))


@router.get("/benchmarks/{benchmark_id}", response_model=ApiResponse[BenchmarkAccountSummary])
def get_benchmark(benchmark_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[BenchmarkAccountSummary]:
    try:
        item = benchmark_service.get_benchmark(user_id, benchmark_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="benchmark not found") from exc
    return ApiResponse(success=True, data=item)


@router.patch("/benchmarks/{benchmark_id}", response_model=ApiResponse[BenchmarkAccountSummary])
def patch_benchmark(benchmark_id: str, payload: BenchmarkPatchRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[BenchmarkAccountSummary]:
    try:
        item = benchmark_service.patch_benchmark(user_id, benchmark_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="benchmark not found") from exc
    return ApiResponse(success=True, data=item)


@router.get("/benchmarks/{benchmark_id}/samples", response_model=ApiResponse[list[BenchmarkContentSample]])
def list_benchmark_samples(benchmark_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[list[BenchmarkContentSample]]:
    return ApiResponse(success=True, data=benchmark_service.list_samples(user_id, benchmark_id))


@router.post("/benchmarks/{benchmark_id}/samples", response_model=ApiResponse[BenchmarkContentSample])
def create_benchmark_sample(benchmark_id: str, payload: BenchmarkSampleCreateRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[BenchmarkContentSample]:
    return ApiResponse(success=True, data=benchmark_service.create_sample(user_id, benchmark_id, payload))


@router.get("/compare/{review_id}", response_model=ApiResponse[dict])
def compare_report(review_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[dict]:
    try:
        gap, plan = benchmark_service.build_gap_to_action(user_id, review_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="review or benchmark not found") from exc
    return ApiResponse(success=True, data={"benchmark_gap_summary": gap, "account_upgrade_plan": plan})
