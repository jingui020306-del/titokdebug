from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.auth import auth_guard
from app.api.deps.rate_limit import rate_limit_guard
from app.core.config import get_settings
from app.schemas.settings import (
    ProviderCredentialCreateRequest,
    ProviderCredentialPatchRequest,
    ProviderCredentialResponse,
    ProviderListResponse,
)
from app.services.provider_credentials_service import provider_credentials_service

router = APIRouter(prefix="/settings/providers", tags=["settings-providers"])


def _to_item(model):
    from app.schemas.settings import ProviderCredentialItem

    return ProviderCredentialItem(
        id=model.id,
        owner_type=model.owner_type,
        provider_name=model.provider_name,
        masked_key=model.masked_key,
        is_active=model.is_active,
        created_at=model.created_at,
    )


@router.get("", response_model=ProviderListResponse)
def list_providers(user_id: str = Depends(auth_guard)) -> ProviderListResponse:
    rate_limit_guard(scope="settings:list")
    settings = get_settings()
    items = [_to_item(x) for x in provider_credentials_service.list_by_owner(user_id)]
    return ProviderListResponse(default_provider_mode=settings.default_provider_mode, items=items)


@router.post("", response_model=ProviderCredentialResponse)
def create_provider(payload: ProviderCredentialCreateRequest, user_id: str = Depends(auth_guard)) -> ProviderCredentialResponse:
    rate_limit_guard(scope="settings:create")
    # Never log payload.api_key.
    item = provider_credentials_service.create(user_id, payload)
    return ProviderCredentialResponse(data=_to_item(item))


@router.patch("/{credential_id}", response_model=ProviderCredentialResponse)
def patch_provider(
    credential_id: str,
    payload: ProviderCredentialPatchRequest,
    user_id: str = Depends(auth_guard),
) -> ProviderCredentialResponse:
    rate_limit_guard(scope="settings:patch")
    try:
        item = provider_credentials_service.patch(user_id, credential_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="provider credential not found") from exc
    return ProviderCredentialResponse(data=_to_item(item))


@router.delete("/{credential_id}")
def delete_provider(credential_id: str, user_id: str = Depends(auth_guard)) -> dict[str, str]:
    rate_limit_guard(scope="settings:delete")
    try:
        provider_credentials_service.delete(user_id, credential_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="provider credential not found") from exc
    return {"status": "deleted"}
