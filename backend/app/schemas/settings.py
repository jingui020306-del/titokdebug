from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

OwnerType = Literal["platform", "user"]
ProviderName = Literal["openai", "anthropic", "qwen", "deepseek", "other"]
ProviderMode = Literal["platform", "byok"]


class ProviderCredentialItem(BaseModel):
    id: str
    owner_type: OwnerType
    provider_name: ProviderName
    masked_key: str
    is_active: bool
    created_at: datetime


class ProviderCredentialCreateRequest(BaseModel):
    owner_type: OwnerType = "user"
    provider_name: ProviderName
    api_key: str = Field(..., min_length=10)
    is_active: bool = False


class ProviderCredentialPatchRequest(BaseModel):
    is_active: bool | None = None


class ProviderListResponse(BaseModel):
    default_provider_mode: ProviderMode
    items: list[ProviderCredentialItem]


class ProviderCredentialResponse(BaseModel):
    data: ProviderCredentialItem
