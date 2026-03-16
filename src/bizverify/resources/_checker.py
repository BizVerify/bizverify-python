from __future__ import annotations

from typing import TYPE_CHECKING

from bizverify._models import CheckerResponse

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncCheckerResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def check(self, entity_name: str, jurisdiction: str) -> CheckerResponse:
        data = self._client.request(
            "POST", "/v1/checker",
            body={"entity_name": entity_name, "jurisdiction": jurisdiction},
            auth="none",
        )
        return CheckerResponse.from_dict(data)  # type: ignore[arg-type]


class AsyncCheckerResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def check(self, entity_name: str, jurisdiction: str) -> CheckerResponse:
        data = await self._client.request(
            "POST", "/v1/checker",
            body={"entity_name": entity_name, "jurisdiction": jurisdiction},
            auth="none",
        )
        return CheckerResponse.from_dict(data)  # type: ignore[arg-type]
