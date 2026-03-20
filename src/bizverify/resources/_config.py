from __future__ import annotations

from typing import TYPE_CHECKING

from bizverify._models import ConfigResponse, JurisdictionsResponse

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncConfigResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def get(self) -> ConfigResponse:
        data = self._client.request("GET", "/v1/config", auth="none")
        return ConfigResponse.from_dict(data)  # type: ignore[arg-type]

    def jurisdictions(self) -> JurisdictionsResponse:
        data = self._client.request("GET", "/v1/jurisdictions", auth="none")
        return JurisdictionsResponse.from_dict(data)  # type: ignore[arg-type]


class AsyncConfigResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get(self) -> ConfigResponse:
        data = await self._client.request("GET", "/v1/config", auth="none")
        return ConfigResponse.from_dict(data)  # type: ignore[arg-type]

    async def jurisdictions(self) -> JurisdictionsResponse:
        data = await self._client.request("GET", "/v1/jurisdictions", auth="none")
        return JurisdictionsResponse.from_dict(data)  # type: ignore[arg-type]
