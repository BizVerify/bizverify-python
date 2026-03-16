from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Iterator

from bizverify._models import SearchResponse, SearchResult
from bizverify._pagination import async_paginate_search, paginate_search

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncSearchResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def find(
        self,
        entity_name: str,
        *,
        jurisdiction: str | None = None,
        entity_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SearchResponse:
        body: dict = {"entity_name": entity_name}
        if jurisdiction is not None:
            body["jurisdiction"] = jurisdiction
        if entity_type is not None:
            body["entity_type"] = entity_type
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        data = self._client.request("POST", "/v1/search", body=body, auth="api_key")
        return SearchResponse.from_dict(data)  # type: ignore[arg-type]

    def find_all(
        self,
        entity_name: str,
        *,
        jurisdiction: str | None = None,
        entity_type: str | None = None,
    ) -> Iterator[SearchResult]:
        return paginate_search(self._client, entity_name, jurisdiction=jurisdiction, entity_type=entity_type)


class AsyncSearchResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def find(
        self,
        entity_name: str,
        *,
        jurisdiction: str | None = None,
        entity_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SearchResponse:
        body: dict = {"entity_name": entity_name}
        if jurisdiction is not None:
            body["jurisdiction"] = jurisdiction
        if entity_type is not None:
            body["entity_type"] = entity_type
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        data = await self._client.request("POST", "/v1/search", body=body, auth="api_key")
        return SearchResponse.from_dict(data)  # type: ignore[arg-type]

    def find_all(
        self,
        entity_name: str,
        *,
        jurisdiction: str | None = None,
        entity_type: str | None = None,
    ) -> AsyncIterator[SearchResult]:
        return async_paginate_search(self._client, entity_name, jurisdiction=jurisdiction, entity_type=entity_type)
