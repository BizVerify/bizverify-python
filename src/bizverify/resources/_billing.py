from __future__ import annotations

from typing import TYPE_CHECKING

from bizverify._models import BillingInfo, PurchaseResponse

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncBillingResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def get(self, *, limit: int | None = None, offset: int | None = None) -> BillingInfo:
        query: dict[str, str] = {}
        if limit is not None:
            query["limit"] = str(limit)
        if offset is not None:
            query["offset"] = str(offset)
        data = self._client.request("GET", "/v1/billing", query=query or None, auth="api_key")
        return BillingInfo.from_dict(data)  # type: ignore[arg-type]

    def purchase(self, package_id: str) -> PurchaseResponse:
        data = self._client.request("POST", "/v1/billing/purchase", body={"package_id": package_id}, auth="api_key")
        return PurchaseResponse.from_dict(data)  # type: ignore[arg-type]


class AsyncBillingResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get(self, *, limit: int | None = None, offset: int | None = None) -> BillingInfo:
        query: dict[str, str] = {}
        if limit is not None:
            query["limit"] = str(limit)
        if offset is not None:
            query["offset"] = str(offset)
        data = await self._client.request("GET", "/v1/billing", query=query or None, auth="api_key")
        return BillingInfo.from_dict(data)  # type: ignore[arg-type]

    async def purchase(self, package_id: str) -> PurchaseResponse:
        data = await self._client.request("POST", "/v1/billing/purchase", body={"package_id": package_id}, auth="api_key")
        return PurchaseResponse.from_dict(data)  # type: ignore[arg-type]
