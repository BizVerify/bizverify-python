from __future__ import annotations

from typing import TYPE_CHECKING

from bizverify._models import RequestAccessResponse, VerifyAccessResponse

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncAuthResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def request_access(self, email: str, accept_terms: bool) -> RequestAccessResponse:
        data = self._client.request(
            "POST", "/v1/auth/request-access",
            body={"email": email, "accept_terms": accept_terms},
            auth="none",
        )
        return RequestAccessResponse.from_dict(data)  # type: ignore[arg-type]

    def verify_access(self, email: str, code: str, label: str | None = None) -> VerifyAccessResponse:
        body: dict[str, object] = {"email": email, "code": code}
        if label is not None:
            body["label"] = label
        data = self._client.request(
            "POST", "/v1/auth/verify-access",
            body=body,
            auth="none",
        )
        resp = VerifyAccessResponse.from_dict(data)  # type: ignore[arg-type]
        self._client.set_api_key(resp.api_key)
        return resp


class AsyncAuthResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def request_access(self, email: str, accept_terms: bool) -> RequestAccessResponse:
        data = await self._client.request(
            "POST", "/v1/auth/request-access",
            body={"email": email, "accept_terms": accept_terms},
            auth="none",
        )
        return RequestAccessResponse.from_dict(data)  # type: ignore[arg-type]

    async def verify_access(self, email: str, code: str, label: str | None = None) -> VerifyAccessResponse:
        body: dict[str, object] = {"email": email, "code": code}
        if label is not None:
            body["label"] = label
        data = await self._client.request(
            "POST", "/v1/auth/verify-access",
            body=body,
            auth="none",
        )
        resp = VerifyAccessResponse.from_dict(data)  # type: ignore[arg-type]
        self._client.set_api_key(resp.api_key)
        return resp
