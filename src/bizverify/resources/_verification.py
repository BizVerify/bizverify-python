from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from bizverify._models import JobStatusResponse, VerificationLevel, VerifyResponse
from bizverify._polling import async_poll_until_complete, poll_until_complete

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncVerificationResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def verify(
        self,
        entity_name: str,
        jurisdiction: str,
        *,
        entity_type: str | None = None,
        verification_level: VerificationLevel | None = None,
        force_refresh: bool | None = None,
        webhook_url: str | None = None,
    ) -> VerifyResponse:
        body: dict[str, Any] = {"entity_name": entity_name, "jurisdiction": jurisdiction}
        if entity_type is not None:
            body["entity_type"] = entity_type
        if verification_level is not None:
            body["verification_level"] = verification_level
        if force_refresh is not None:
            body["force_refresh"] = force_refresh
        if webhook_url is not None:
            body["webhook_url"] = webhook_url
        data = self._client.request("POST", "/v1/verify", body=body, auth="api_key")
        return VerifyResponse.from_dict(data)  # type: ignore[arg-type]

    def verify_and_wait(
        self,
        entity_name: str,
        jurisdiction: str,
        *,
        entity_type: str | None = None,
        verification_level: VerificationLevel | None = None,
        force_refresh: bool | None = None,
        webhook_url: str | None = None,
        poll_interval: float = 2.0,
        timeout: float = 60.0,
        on_status_change: Callable[[JobStatusResponse], Any] | None = None,
    ) -> JobStatusResponse:
        resp = self.verify(
            entity_name, jurisdiction,
            entity_type=entity_type, verification_level=verification_level,
            force_refresh=force_refresh, webhook_url=webhook_url,
        )
        return poll_until_complete(
            self._client, resp,
            poll_interval=poll_interval, timeout=timeout, on_status_change=on_status_change,
        )

    def get_status(self, job_id: str) -> JobStatusResponse:
        data = self._client.request("GET", f"/v1/verify/status/{job_id}", auth="api_key")
        return JobStatusResponse.from_dict(data)  # type: ignore[arg-type]


class AsyncVerificationResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def verify(
        self,
        entity_name: str,
        jurisdiction: str,
        *,
        entity_type: str | None = None,
        verification_level: VerificationLevel | None = None,
        force_refresh: bool | None = None,
        webhook_url: str | None = None,
    ) -> VerifyResponse:
        body: dict[str, Any] = {"entity_name": entity_name, "jurisdiction": jurisdiction}
        if entity_type is not None:
            body["entity_type"] = entity_type
        if verification_level is not None:
            body["verification_level"] = verification_level
        if force_refresh is not None:
            body["force_refresh"] = force_refresh
        if webhook_url is not None:
            body["webhook_url"] = webhook_url
        data = await self._client.request("POST", "/v1/verify", body=body, auth="api_key")
        return VerifyResponse.from_dict(data)  # type: ignore[arg-type]

    async def verify_and_wait(
        self,
        entity_name: str,
        jurisdiction: str,
        *,
        entity_type: str | None = None,
        verification_level: VerificationLevel | None = None,
        force_refresh: bool | None = None,
        webhook_url: str | None = None,
        poll_interval: float = 2.0,
        timeout: float = 60.0,
        on_status_change: Callable[[JobStatusResponse], Any] | None = None,
    ) -> JobStatusResponse:
        resp = await self.verify(
            entity_name, jurisdiction,
            entity_type=entity_type, verification_level=verification_level,
            force_refresh=force_refresh, webhook_url=webhook_url,
        )
        return await async_poll_until_complete(
            self._client, resp,
            poll_interval=poll_interval, timeout=timeout, on_status_change=on_status_change,
        )

    async def get_status(self, job_id: str) -> JobStatusResponse:
        data = await self._client.request("GET", f"/v1/verify/status/{job_id}", auth="api_key")
        return JobStatusResponse.from_dict(data)  # type: ignore[arg-type]
