from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.auth import auth_guard
from app.schemas.common import ApiResponse, ContentItemSummary, ContentVersionSummary
from app.schemas.content_studio import ContentItemDetail, ContentItemTimeline, ContentRewriteRequest, MarkPublishedRequest, NextPostRecommendationSummary, WeeklyPlanRequest
from app.services.content_studio_service import content_studio_service
from app.services.rewrite_engine_service import rewrite_engine_service

router = APIRouter(prefix="/content-studio", tags=["content-studio"])


@router.post("/plan/mock-create")
def create_plan(payload: WeeklyPlanRequest, user_id: str = Depends(auth_guard)) -> dict[str, str]:
    plan_id = content_studio_service.create_weekly_plan(user_id, payload)
    return {"plan_id": plan_id, "status": "created"}


@router.get("/plan/{plan_id}")
def get_plan(plan_id: str, user_id: str = Depends(auth_guard)):
    report = content_studio_service.get_weekly_plan(user_id, plan_id)
    if not report:
        raise HTTPException(status_code=404, detail="plan not found")
    return {"status": "ready", "data": report}


@router.post("/rewrite/mock-create")
def rewrite_create(payload: ContentRewriteRequest, user_id: str = Depends(auth_guard)) -> dict[str, str]:
    rw_payload = {
        "platform": payload.platform,
        "goal": "转咨询" if payload.goal_action == "转咨询" else "涨粉",
        "original_title": payload.original_title,
        "original_script": payload.original_script,
        "original_cover_text": payload.original_cover_text,
        "current_issues": ["前3秒弱"],
        "style_limits": payload.risk_limits[:2],
        "industry": payload.pillar,
        "target_audience": payload.target_audience,
    }
    from app.schemas.rewrite_engine import RewriteInput

    job_id = rewrite_engine_service.create_mock(user_id, RewriteInput(**rw_payload))
    report = rewrite_engine_service.get_report(job_id, user_id)
    if report:
        content_studio_service.create_or_update_version_from_rewrite(
            user_id,
            rewrite_id=job_id,
            content_item_id=payload.content_item_id,
            title=payload.original_title,
            pillar=payload.pillar,
            cover_text=payload.original_cover_text,
            hook=report.hook_variants[0].content if report.hook_variants else "",
            body_script=report.body_script,
            closing_cta=report.closing_cta,
            comment_guide=report.comment_guide,
            risk_notes="；".join(f"{x.raw}->{x.safe}" for x in report.risk_replacements),
        )
    return {"rewrite_id": job_id, "status": "created"}


@router.get("/rewrite/{rewrite_id}")
def rewrite_report(rewrite_id: str, user_id: str = Depends(auth_guard)):
    report = rewrite_engine_service.get_report(rewrite_id, user_id)
    if not report:
        raise HTTPException(status_code=404, detail="rewrite not found")
    return {"status": "ready", "data": report}


@router.post("/rewrite/{rewrite_id}/adopt")
def adopt_rewrite(rewrite_id: str, user_id: str = Depends(auth_guard)) -> dict[str, str]:
    report = rewrite_engine_service.get_report(rewrite_id, user_id)
    if not report:
        raise HTTPException(status_code=404, detail="rewrite not found")
    version_id = content_studio_service.create_or_update_version_from_rewrite(
        user_id,
        rewrite_id=rewrite_id,
        content_item_id=None,
        title=report.rewrite_input.original_title,
        pillar=report.rewrite_input.industry,
        cover_text=report.rewrite_input.original_cover_text,
        hook=report.hook_variants[0].content if report.hook_variants else "",
        body_script=report.body_script,
        closing_cta=report.closing_cta,
        comment_guide=report.comment_guide,
        risk_notes="；".join(f"{x.raw}->{x.safe}" for x in report.risk_replacements),
    )
    return {"status": "ok", "message": "已标记为采用，可进入复盘台。", "version_id": version_id}


@router.get("/history")
def history(user_id: str = Depends(auth_guard)):
    return {"items": content_studio_service.get_history(user_id)}


@router.get("/items", response_model=ApiResponse[list[ContentItemSummary]])
def list_content_items(user_id: str = Depends(auth_guard)) -> ApiResponse[list[ContentItemSummary]]:
    return ApiResponse(success=True, data=content_studio_service.list_items(user_id))


@router.get("/items/{item_id}", response_model=ApiResponse[ContentItemDetail])
def get_content_item(item_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[ContentItemDetail]:
    detail = content_studio_service.get_item_detail(user_id, item_id)
    if not detail:
        raise HTTPException(status_code=404, detail="content item not found")
    return ApiResponse(success=True, data=detail)


@router.get("/items/{item_id}/versions", response_model=ApiResponse[list[ContentVersionSummary]])
def get_content_versions(item_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[list[ContentVersionSummary]]:
    return ApiResponse(success=True, data=content_studio_service.list_versions(user_id, item_id))


@router.get("/items/{item_id}/timeline", response_model=ApiResponse[ContentItemTimeline])
def get_content_timeline(item_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[ContentItemTimeline]:
    return ApiResponse(success=True, data=content_studio_service.get_item_timeline(user_id, item_id))


@router.post("/items/{item_id}/mark-published", response_model=ApiResponse[dict[str, str]])
def mark_item_published(item_id: str, payload: MarkPublishedRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[dict[str, str]]:
    try:
        record_id = content_studio_service.mark_published(user_id, item_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="content item not found") from exc
    return ApiResponse(success=True, data={"item_id": item_id, "publish_record_id": record_id})


@router.post("/items/{item_id}/archive", response_model=ApiResponse[dict[str, str]])
def archive_item(item_id: str, user_id: str = Depends(auth_guard)) -> ApiResponse[dict[str, str]]:
    if not content_studio_service.archive_item(user_id, item_id):
        raise HTTPException(status_code=404, detail="content item not found")
    return ApiResponse(success=True, data={"item_id": item_id, "status": "archived"})


@router.get("/next-post", response_model=ApiResponse[NextPostRecommendationSummary])
def get_next_post(user_id: str = Depends(auth_guard)) -> ApiResponse[NextPostRecommendationSummary]:
    return ApiResponse(success=True, data=content_studio_service.get_next_post_recommendation(user_id))
