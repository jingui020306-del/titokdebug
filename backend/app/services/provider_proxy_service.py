from __future__ import annotations

from app.api.deps.rate_limit import rate_limit_guard


class ProviderProxyService:
    def invoke(self, provider_name: str, payload: dict, *, owner_id: str) -> dict:
        """Centralized provider proxy placeholder.

        TODO: Route all future LLM/provider traffic through this service.
        TODO: Attach auth context, credential resolution, audit log and structured retries.
        """
        rate_limit_guard(scope=f"provider:{provider_name}:{owner_id}")
        return {
            "status": "placeholder",
            "provider": provider_name,
            "message": "Provider proxy not wired to real model APIs yet.",
            "payload_preview": {k: payload[k] for k in list(payload)[:3]},
        }


provider_proxy_service = ProviderProxyService()
