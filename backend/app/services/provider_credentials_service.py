from __future__ import annotations

import base64
import uuid
from datetime import datetime, timezone

from app.core.db import get_conn
from app.models import ProviderCredential
from app.schemas.settings import ProviderCredentialCreateRequest, ProviderCredentialPatchRequest


class ProviderCredentialsService:
    def list_by_owner(self, owner_id: str) -> list[ProviderCredential]:
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM provider_credentials WHERE owner_id = ? ORDER BY created_at DESC", (owner_id,)).fetchall()
        return [self._to_model(row) for row in rows]

    def create(self, owner_id: str, payload: ProviderCredentialCreateRequest) -> ProviderCredential:
        if payload.is_active:
            self._clear_active(owner_id)

        raw_key = payload.api_key.strip()
        item = ProviderCredential(
            id=f"pc_{uuid.uuid4().hex[:10]}",
            owner_id=owner_id,
            owner_type=payload.owner_type,
            provider_name=payload.provider_name,
            masked_key=self._mask(raw_key),
            encrypted_key=self._encrypt(raw_key),
            is_active=payload.is_active,
            created_at=datetime.now(timezone.utc),
        )
        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO provider_credentials (id, owner_id, owner_type, provider_name, masked_key, encrypted_key, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (item.id, item.owner_id, item.owner_type, item.provider_name, item.masked_key, item.encrypted_key, int(item.is_active), item.created_at.isoformat()),
            )
        return item

    def patch(self, owner_id: str, credential_id: str, payload: ProviderCredentialPatchRequest) -> ProviderCredential:
        item = self._must_get(owner_id, credential_id)
        if payload.is_active is not None:
            if payload.is_active:
                self._clear_active(owner_id)
            with get_conn() as conn:
                conn.execute("UPDATE provider_credentials SET is_active = ? WHERE id = ?", (int(payload.is_active), credential_id))
        return self._must_get(owner_id, credential_id)

    def delete(self, owner_id: str, credential_id: str) -> None:
        self._must_get(owner_id, credential_id)
        with get_conn() as conn:
            conn.execute("DELETE FROM provider_credentials WHERE id = ?", (credential_id,))

    def _must_get(self, owner_id: str, credential_id: str) -> ProviderCredential:
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM provider_credentials WHERE id = ? AND owner_id = ?", (credential_id, owner_id)).fetchone()
        if not row:
            raise KeyError(credential_id)
        return self._to_model(row)

    def _clear_active(self, owner_id: str) -> None:
        with get_conn() as conn:
            conn.execute("UPDATE provider_credentials SET is_active = 0 WHERE owner_id = ?", (owner_id,))

    @staticmethod
    def _mask(raw_key: str) -> str:
        if len(raw_key) <= 8:
            return "****"
        return f"{raw_key[:4]}****{raw_key[-4:]}"

    @staticmethod
    def _encrypt(raw_key: str) -> str:
        # TODO: Replace with production encryption using KMS/HSM or env-managed master key.
        return base64.b64encode(raw_key.encode("utf-8")).decode("utf-8")

    @staticmethod
    def _to_model(row) -> ProviderCredential:
        return ProviderCredential(
            id=row["id"],
            owner_id=row["owner_id"],
            owner_type=row["owner_type"],
            provider_name=row["provider_name"],
            masked_key=row["masked_key"],
            encrypted_key=row["encrypted_key"],
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )


provider_credentials_service = ProviderCredentialsService()
