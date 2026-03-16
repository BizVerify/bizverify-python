from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Iterator

from bizverify._models import SearchResponse, SearchResult

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient

DEFAULT_PAGE_SIZE = 50


def paginate_search(
    client: SyncHttpClient,
    entity_name: str,
    *,
    jurisdiction: str | None = None,
    entity_type: str | None = None,
) -> Iterator[SearchResult]:
    offset = 0
    limit = DEFAULT_PAGE_SIZE

    while True:
        body: dict = {"entity_name": entity_name, "limit": limit, "offset": offset}
        if jurisdiction is not None:
            body["jurisdiction"] = jurisdiction
        if entity_type is not None:
            body["entity_type"] = entity_type

        data = client.request("POST", "/v1/search", body=body, auth="api_key")
        resp = SearchResponse.from_dict(data)  # type: ignore[arg-type]

        yield from resp.results

        if not resp.results or offset + len(resp.results) >= resp.total:
            break

        offset += len(resp.results)


async def async_paginate_search(
    client: AsyncHttpClient,
    entity_name: str,
    *,
    jurisdiction: str | None = None,
    entity_type: str | None = None,
) -> AsyncIterator[SearchResult]:
    offset = 0
    limit = DEFAULT_PAGE_SIZE

    while True:
        body: dict = {"entity_name": entity_name, "limit": limit, "offset": offset}
        if jurisdiction is not None:
            body["jurisdiction"] = jurisdiction
        if entity_type is not None:
            body["entity_type"] = entity_type

        data = await client.request("POST", "/v1/search", body=body, auth="api_key")
        resp = SearchResponse.from_dict(data)  # type: ignore[arg-type]

        for result in resp.results:
            yield result

        if not resp.results or offset + len(resp.results) >= resp.total:
            break

        offset += len(resp.results)
