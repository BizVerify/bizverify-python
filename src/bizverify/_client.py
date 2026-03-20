from __future__ import annotations

import json
import time
from typing import Any

import httpx

from bizverify._errors import BizVerifyError, TimeoutError, parse_error_response
from bizverify._models import ResponseMeta

DEFAULT_BASE_URL = "https://api.bizverify.co"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2


def _parse_int_header(headers: httpx.Headers, name: str) -> int | None:
    value = headers.get(name)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


class SyncHttpClient:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        max_retries: int | None = None,
        timeout: float | None = None,
    ) -> None:
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._max_retries = max_retries if max_retries is not None else DEFAULT_MAX_RETRIES
        self._timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        self._api_key = api_key
        self._client = httpx.Client(timeout=self._timeout)
        self._last_response_meta: ResponseMeta | None = None

    def set_api_key(self, api_key: str) -> None:
        self._api_key = api_key

    @property
    def last_response_meta(self) -> ResponseMeta | None:
        return self._last_response_meta

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Any = None,
        query: dict[str, str] | None = None,
        auth: str = "api_key",
    ) -> dict[str, Any] | None:
        url = self._build_url(path, query)
        headers = self._build_headers(auth, body is not None)
        content = json.dumps(body).encode() if body is not None else None

        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            if attempt > 0:
                delay = min(1.0 * 2 ** (attempt - 1), 4.0)
                time.sleep(delay)

            try:
                response = self._client.request(method, url, headers=headers, content=content)

                self._last_response_meta = ResponseMeta(
                    credits_remaining=_parse_int_header(response.headers, "x-credits-remaining"),
                    credits_charged=_parse_int_header(response.headers, "x-credits-charged"),
                    rate_limit_limit=_parse_int_header(response.headers, "x-ratelimit-limit"),
                    rate_limit_remaining=_parse_int_header(response.headers, "x-ratelimit-remaining"),
                    rate_limit_reset=_parse_int_header(response.headers, "x-ratelimit-reset"),
                )

                if response.status_code == 204:
                    return None

                response_body = response.json()

                if response.status_code >= 400:
                    error = parse_error_response(response.status_code, response_body, response.headers)
                    if response.status_code >= 500 and attempt < self._max_retries:
                        last_error = error
                        continue
                    raise error

                return response_body
            except BizVerifyError:
                raise
            except httpx.TimeoutException:
                last_error = TimeoutError("Request timed out")
                if attempt < self._max_retries:
                    continue
                raise last_error
            except Exception as exc:
                last_error = BizVerifyError(str(exc), "NETWORK_ERROR", 0)
                if attempt < self._max_retries:
                    continue
                raise last_error

        raise last_error or BizVerifyError("Request failed", "UNKNOWN", 0)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> SyncHttpClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _build_url(self, path: str, query: dict[str, str] | None) -> str:
        url = f"{self._base_url}{path}"
        if query:
            params = "&".join(f"{k}={v}" for k, v in query.items() if v is not None)
            if params:
                url = f"{url}?{params}"
        return url

    def _build_headers(self, auth: str, has_body: bool) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if has_body:
            headers["Content-Type"] = "application/json"
        if auth == "api_key" and self._api_key:
            headers["X-API-Key"] = self._api_key
        return headers


class AsyncHttpClient:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        max_retries: int | None = None,
        timeout: float | None = None,
    ) -> None:
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._max_retries = max_retries if max_retries is not None else DEFAULT_MAX_RETRIES
        self._timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        self._api_key = api_key
        self._client = httpx.AsyncClient(timeout=self._timeout)
        self._last_response_meta: ResponseMeta | None = None

    def set_api_key(self, api_key: str) -> None:
        self._api_key = api_key

    @property
    def last_response_meta(self) -> ResponseMeta | None:
        return self._last_response_meta

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: Any = None,
        query: dict[str, str] | None = None,
        auth: str = "api_key",
    ) -> dict[str, Any] | None:
        import asyncio

        url = self._build_url(path, query)
        headers = self._build_headers(auth, body is not None)
        content = json.dumps(body).encode() if body is not None else None

        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            if attempt > 0:
                delay = min(1.0 * 2 ** (attempt - 1), 4.0)
                await asyncio.sleep(delay)

            try:
                response = await self._client.request(method, url, headers=headers, content=content)

                self._last_response_meta = ResponseMeta(
                    credits_remaining=_parse_int_header(response.headers, "x-credits-remaining"),
                    credits_charged=_parse_int_header(response.headers, "x-credits-charged"),
                    rate_limit_limit=_parse_int_header(response.headers, "x-ratelimit-limit"),
                    rate_limit_remaining=_parse_int_header(response.headers, "x-ratelimit-remaining"),
                    rate_limit_reset=_parse_int_header(response.headers, "x-ratelimit-reset"),
                )

                if response.status_code == 204:
                    return None

                response_body = response.json()

                if response.status_code >= 400:
                    error = parse_error_response(response.status_code, response_body, response.headers)
                    if response.status_code >= 500 and attempt < self._max_retries:
                        last_error = error
                        continue
                    raise error

                return response_body
            except BizVerifyError:
                raise
            except httpx.TimeoutException:
                last_error = TimeoutError("Request timed out")
                if attempt < self._max_retries:
                    continue
                raise last_error
            except Exception as exc:
                last_error = BizVerifyError(str(exc), "NETWORK_ERROR", 0)
                if attempt < self._max_retries:
                    continue
                raise last_error

        raise last_error or BizVerifyError("Request failed", "UNKNOWN", 0)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    def _build_url(self, path: str, query: dict[str, str] | None) -> str:
        url = f"{self._base_url}{path}"
        if query:
            params = "&".join(f"{k}={v}" for k, v in query.items() if v is not None)
            if params:
                url = f"{url}?{params}"
        return url

    def _build_headers(self, auth: str, has_body: bool) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if has_body:
            headers["Content-Type"] = "application/json"
        if auth == "api_key" and self._api_key:
            headers["X-API-Key"] = self._api_key
        return headers
