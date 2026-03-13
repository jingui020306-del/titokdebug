from fastapi import APIRouter, Depends

from app.api.deps.auth import auth_guard
from app.schemas.account_audit import MockCreateResponse
from app.schemas.niche_map import BenchmarkAccount, NicheInput
from app.schemas.rewrite_engine import RewriteInput
from app.services.account_audit_service import account_audit_service
from app.services.niche_map_service import niche_map_service
from app.services.rewrite_engine_service import rewrite_engine_service

router = APIRouter(prefix="/dev", tags=["dev"])


@router.post("/seed-account-audit-demo", response_model=MockCreateResponse)
def seed_account_audit_demo(user_id: str = Depends(auth_guard)) -> MockCreateResponse:
    job_id = account_audit_service.create_seed_job(user_id=user_id)
    return MockCreateResponse(job_id=job_id, status="created", message="Seed 账户体检任务创建成功")


@router.post("/seed-all-demo")
def seed_all_demo(user_id: str = Depends(auth_guard)) -> dict[str, str]:
    account_audit_job_id = account_audit_service.create_seed_job(user_id=user_id)

    niche_payload = NicheInput(
        platform="抖音",
        niche_keyword="职场表达",
        goal="涨粉",
        target_audience="3-8年经验管理者",
        current_offer="表达咨询+训练营",
        benchmark_accounts=[BenchmarkAccount(handle="bench_01"), BenchmarkAccount(handle="bench_02"), BenchmarkAccount(handle="bench_03")],
        current_stage="起量中",
        risk_limits="避免夸大承诺",
    )
    niche_map_job_id = niche_map_service.create_mock(user_id=user_id, payload=niche_payload)

    rewrite_payload = RewriteInput(
        platform="抖音",
        goal="涨粉",
        original_title="表达能力怎么提升",
        original_script="今天讲一个表达技巧。",
        original_cover_text="表达技巧",
        current_issues=["标题太平", "前3秒弱"],
        style_limits=["避免强营销"],
        industry="职业教育",
        target_audience="职场管理者",
    )
    rewrite_engine_job_id = rewrite_engine_service.create_mock(user_id=user_id, payload=rewrite_payload)

    return {
        "status": "ok",
        "account_audit_job_id": account_audit_job_id,
        "niche_map_job_id": niche_map_job_id,
        "rewrite_engine_job_id": rewrite_engine_job_id,
    }
