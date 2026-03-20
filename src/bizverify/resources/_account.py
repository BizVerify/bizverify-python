from __future__ import annotations

from typing import TYPE_CHECKING

from bizverify._models import Account, CreateKeyResponse, DataExport, MessageResponse, UsageStats

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncAccountResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def get(self) -> Account:
        data = self._client.request("GET", "/v1/account", auth="api_key")
        return Account.from_dict(data)  # type: ignore[arg-type]

    def usage(self, *, days: int | None = None) -> UsageStats:
        query: dict[str, str] = {}
        if days is not None:
            query["days"] = str(days)
        data = self._client.request("GET", "/v1/account/usage", query=query or None, auth="api_key")
        return UsageStats.from_dict(data)  # type: ignore[arg-type]

    def data_export(self) -> DataExport:
        data = self._client.request("GET", "/v1/account/data-export", auth="api_key")
        return DataExport.from_dict(data)  # type: ignore[arg-type]

    def update_email(self, email: str) -> MessageResponse:
        data = self._client.request("PATCH", "/v1/account", body={"email": email}, auth="api_key")
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    def create_key(self, label: str) -> CreateKeyResponse:
        data = self._client.request("POST", "/v1/account/keys", body={"label": label}, auth="api_key")
        return CreateKeyResponse.from_dict(data)  # type: ignore[arg-type]

    def revoke_key(self, key_id: str) -> None:
        self._client.request("DELETE", f"/v1/account/keys/{key_id}", auth="api_key")


class AsyncAccountResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get(self) -> Account:
        data = await self._client.request("GET", "/v1/account", auth="api_key")
        return Account.from_dict(data)  # type: ignore[arg-type]

    async def usage(self, *, days: int | None = None) -> UsageStats:
        query: dict[str, str] = {}
        if days is not None:
            query["days"] = str(days)
        data = await self._client.request("GET", "/v1/account/usage", query=query or None, auth="api_key")
        return UsageStats.from_dict(data)  # type: ignore[arg-type]

    async def data_export(self) -> DataExport:
        data = await self._client.request("GET", "/v1/account/data-export", auth="api_key")
        return DataExport.from_dict(data)  # type: ignore[arg-type]

    async def update_email(self, email: str) -> MessageResponse:
        data = await self._client.request("PATCH", "/v1/account", body={"email": email}, auth="api_key")
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    async def create_key(self, label: str) -> CreateKeyResponse:
        data = await self._client.request("POST", "/v1/account/keys", body={"label": label}, auth="api_key")
        return CreateKeyResponse.from_dict(data)  # type: ignore[arg-type]

    async def revoke_key(self, key_id: str) -> None:
        await self._client.request("DELETE", f"/v1/account/keys/{key_id}", auth="api_key")
