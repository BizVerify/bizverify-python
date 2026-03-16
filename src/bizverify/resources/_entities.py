from __future__ import annotations

from typing import TYPE_CHECKING

from bizverify._models import Entity, PaginatedSnapshots

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncEntitiesResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def get(self, entity_id: str) -> Entity:
        data = self._client.request("GET", f"/v1/entity/{entity_id}", auth="api_key")
        return Entity.from_dict(data)  # type: ignore[arg-type]

    def history(self, entity_id: str, *, limit: int | None = None, offset: int | None = None) -> PaginatedSnapshots:
        query: dict[str, str] = {}
        if limit is not None:
            query["limit"] = str(limit)
        if offset is not None:
            query["offset"] = str(offset)
        data = self._client.request("GET", f"/v1/entity/{entity_id}/history", query=query or None, auth="api_key")
        return PaginatedSnapshots.from_dict(data)  # type: ignore[arg-type]


class AsyncEntitiesResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get(self, entity_id: str) -> Entity:
        data = await self._client.request("GET", f"/v1/entity/{entity_id}", auth="api_key")
        return Entity.from_dict(data)  # type: ignore[arg-type]

    async def history(self, entity_id: str, *, limit: int | None = None, offset: int | None = None) -> PaginatedSnapshots:
        query: dict[str, str] = {}
        if limit is not None:
            query["limit"] = str(limit)
        if offset is not None:
            query["offset"] = str(offset)
        data = await self._client.request("GET", f"/v1/entity/{entity_id}/history", query=query or None, auth="api_key")
        return PaginatedSnapshots.from_dict(data)  # type: ignore[arg-type]
