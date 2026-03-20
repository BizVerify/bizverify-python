from __future__ import annotations

import httpx
import pytest
import respx

from bizverify._client import AsyncHttpClient
from bizverify._errors import ValidationError

BASE = "https://api.bizverify.co"


@pytest.mark.asyncio
async def test_async_successful_get():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/account").mock(return_value=httpx.Response(200, json={"id": "123"}))
        client = AsyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
        result = await client.request("GET", "/v1/account", auth="api_key")
        assert result == {"id": "123"}
        await client.close()


@pytest.mark.asyncio
async def test_async_204_returns_none():
    with respx.mock(base_url=BASE) as mock:
        mock.delete("/v1/account/keys/k1").mock(return_value=httpx.Response(204))
        client = AsyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
        result = await client.request("DELETE", "/v1/account/keys/k1", auth="api_key")
        assert result is None
        await client.close()


@pytest.mark.asyncio
async def test_async_error_response():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/test").mock(
            return_value=httpx.Response(400, json={"error": {"code": "BAD", "message": "bad"}})
        )
        client = AsyncHttpClient(base_url=BASE, max_retries=0)
        with pytest.raises(ValidationError):
            await client.request("GET", "/v1/test", auth="none")
        await client.close()


@pytest.mark.asyncio
async def test_async_retry_on_500():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            return httpx.Response(500, json={"error": {"code": "INTERNAL", "message": "fail"}})
        return httpx.Response(200, json={"ok": True})

    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/test").mock(side_effect=handler)
        client = AsyncHttpClient(base_url=BASE, max_retries=1)
        result = await client.request("GET", "/v1/test", auth="none")
        assert result == {"ok": True}
        assert call_count == 2
        await client.close()


@pytest.mark.asyncio
async def test_async_context_manager():
    async with AsyncHttpClient(base_url=BASE) as client:
        assert isinstance(client, AsyncHttpClient)


@pytest.mark.asyncio
async def test_async_last_response_meta():
    headers = {
        "x-credits-remaining": "42",
        "x-credits-charged": "2",
    }
    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/test").mock(return_value=httpx.Response(200, json={}, headers=headers))
        client = AsyncHttpClient(base_url=BASE, max_retries=0)
        await client.request("GET", "/v1/test", auth="none")
        meta = client.last_response_meta
        assert meta is not None
        assert meta.credits_remaining == 42
        assert meta.credits_charged == 2
        await client.close()
