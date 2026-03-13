from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

OwnerType = Literal["platform", "user"]
ProviderName = Literal["openai", "anthropic", "qwen", "deepseek", "other"]


@dataclass
class ProviderCredential:
    id: str
    owner_id: str
    owner_type: OwnerType
    provider_name: ProviderName
    masked_key: str
    encrypted_key: str
    is_active: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
