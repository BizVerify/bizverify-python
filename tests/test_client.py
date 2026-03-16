from __future__ import annotations

import httpx
import pytest
import respx

from bizverify._client import SyncHttpClient
from bizverify._errors import BizVerifyError, InternalError, ValidationError

BASE = "https://api.bizverify.co"


def test_successful_get(mock_api, sync_client):
    mock_api.get("/v1/account").mock(return_value=httpx.Response(200, json={"id": "123"}))
    result = sync_client.request("GET", "/v1/account", auth="jwt")
    assert result == {"id": "123"}


def test_successful_post(mock_api, sync_client):
    mock_api.post("/v1/verify").mock(return_value=httpx.Response(200, json={"status": "pending"}))
    result = sync_client.request("POST", "/v1/verify", body={"entity_name": "Acme"}, auth="api_key")
    assert result == {"status": "pending"}


def test_204_returns_none(mock_api, sync_client):
    mock_api.delete("/v1/account").mock(return_value=httpx.Response(204))
    result = sync_client.request("DELETE", "/v1/account", body={"password": "x"}, auth="jwt")
    assert result is None


def test_error_response(mock_api, sync_client):
    mock_api.get("/v1/account").mock(
        return_value=httpx.Response(400, json={"error": {"code": "VALIDATION_ERROR", "message": "Bad"}})
    )
    with pytest.raises(ValidationError) as exc_info:
        sync_client.request("GET", "/v1/account", auth="jwt")
    assert exc_info.value.code == "VALIDATION_ERROR"


def test_retry_on_500():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return httpx.Response(500, json={"error": {"code": "INTERNAL", "message": "fail"}})
        return httpx.Response(200, json={"ok": True})

    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/test").mock(side_effect=handler)
        client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=2, timeout=5.0)
        result = client.request("GET", "/v1/test")
        assert result == {"ok": True}
        assert call_count == 3
        client.close()


def test_no_retry_on_400(mock_api):
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        return httpx.Response(400, json={"error": {"code": "BAD", "message": "bad"}})

    mock_api.get("/v1/test").mock(side_effect=handler)
    client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=2)
    with pytest.raises(ValidationError):
        client.request("GET", "/v1/test")
    assert call_count == 1
    client.close()


def test_api_key_header(mock_api):
    def handler(request):
        assert request.headers["X-API-Key"] == "my-key"
        return httpx.Response(200, json={})

    mock_api.get("/v1/test").mock(side_effect=handler)
    client = SyncHttpClient(base_url=BASE, api_key="my-key")
    client.request("GET", "/v1/test", auth="api_key")
    client.close()


def test_jwt_header(mock_api):
    def handler(request):
        assert request.headers["Authorization"] == "Bearer my-token"
        return httpx.Response(200, json={})

    mock_api.get("/v1/test").mock(side_effect=handler)
    client = SyncHttpClient(base_url=BASE, token="my-token")
    client.request("GET", "/v1/test", auth="jwt")
    client.close()


def test_no_auth_header(mock_api):
    def handler(request):
        assert "X-API-Key" not in request.headers
        assert "Authorization" not in request.headers
        return httpx.Response(200, json={})

    mock_api.get("/v1/test").mock(side_effect=handler)
    client = SyncHttpClient(base_url=BASE)
    client.request("GET", "/v1/test", auth="none")
    client.close()


def test_query_params(mock_api, sync_client):
    def handler(request):
        assert "days=30" in str(request.url)
        return httpx.Response(200, json={})

    mock_api.get("/v1/account/usage").mock(side_effect=handler)
    sync_client.request("GET", "/v1/account/usage", query={"days": "30"}, auth="jwt")


def test_set_token(sync_client):
    sync_client.set_token("new-token")
    assert sync_client._token == "new-token"


def test_set_api_key(sync_client):
    sync_client.set_api_key("new-key")
    assert sync_client._api_key == "new-key"


def test_context_manager():
    client = SyncHttpClient(base_url=BASE)
    with client as c:
        assert c is client
    # After exit, client should be closed (no assertion needed, just no error)
