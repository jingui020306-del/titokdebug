from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps.auth import auth_guard
from app.schemas.common import ApiResponse
from app.schemas.workspace import WorkspaceSummary, WorkspaceTimeline
from app.services.workspace_service import workspace_service

router = APIRouter(prefix="/workspace", tags=["workspace"])


class TodoStatusUpdateRequest(BaseModel):
    status: str


@router.get("/summary", response_model=ApiResponse[WorkspaceSummary])
def get_workspace_summary(user_id: str = Depends(auth_guard)) -> ApiResponse[WorkspaceSummary]:
    return ApiResponse(success=True, data=workspace_service.get_summary(user_id))


@router.get("/timeline", response_model=ApiResponse[WorkspaceTimeline])
def get_workspace_timeline(user_id: str = Depends(auth_guard)) -> ApiResponse[WorkspaceTimeline]:
    return ApiResponse(success=True, data=workspace_service.get_timeline(user_id))


@router.patch("/todos/{todo_id}", response_model=ApiResponse[dict[str, str]])
def patch_workspace_todo(todo_id: str, payload: TodoStatusUpdateRequest, user_id: str = Depends(auth_guard)) -> ApiResponse[dict[str, str]]:
    ok = workspace_service.update_todo_status(user_id=user_id, todo_id=todo_id, status=payload.status)
    if not ok:
        raise HTTPException(status_code=404, detail="todo not found")
    return ApiResponse(success=True, data={"todo_id": todo_id, "status": payload.status})
