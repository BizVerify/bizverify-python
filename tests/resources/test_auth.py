from __future__ import annotations

import httpx

from bizverify._client import SyncHttpClient
from bizverify.resources._auth import SyncAuthResource
from tests.fixtures import REQUEST_ACCESS_RESPONSE, VERIFY_ACCESS_RESPONSE

BASE = "https://api.bizverify.co"


def test_request_access(mock_api, sync_client):
    def handler(request):
        body = request.content.decode()
        assert '"email": "test@example.com"' in body or '"email":"test@example.com"' in body
        assert "accept_terms" in body
        return httpx.Response(200, json=REQUEST_ACCESS_RESPONSE)

    mock_api.post("/v1/auth/request-access").mock(side_effect=handler)
    resource = SyncAuthResource(sync_client)
    resp = resource.request_access("test@example.com", True)
    assert resp.message == "Verification code sent to test@example.com"


def test_verify_access(mock_api, sync_client):
    mock_api.post("/v1/auth/verify-access").mock(return_value=httpx.Response(200, json=VERIFY_ACCESS_RESPONSE))
    resource = SyncAuthResource(sync_client)
    resp = resource.verify_access("test@example.com", "123456")
    assert resp.api_key == "bv_live_abc123def456"
    assert resp.key_id == "key_001"
    assert resp.label == "key-1710000000"


def test_verify_access_sets_api_key(mock_api, sync_client):
    mock_api.post("/v1/auth/verify-access").mock(return_value=httpx.Response(200, json=VERIFY_ACCESS_RESPONSE))
    resource = SyncAuthResource(sync_client)
    resource.verify_access("test@example.com", "123456")
    assert sync_client._api_key == "bv_live_abc123def456"


def test_verify_access_with_label(mock_api, sync_client):
    def handler(request):
        body = request.content.decode()
        assert '"label": "my-agent"' in body or '"label":"my-agent"' in body
        return httpx.Response(200, json=VERIFY_ACCESS_RESPONSE)

    mock_api.post("/v1/auth/verify-access").mock(side_effect=handler)
    resource = SyncAuthResource(sync_client)
    resource.verify_access("test@example.com", "123456", label="my-agent")


def test_request_access_no_auth_header(mock_api, sync_client):
    def handler(request):
        assert "X-API-Key" not in request.headers
        assert "Authorization" not in request.headers
        return httpx.Response(200, json=REQUEST_ACCESS_RESPONSE)

    mock_api.post("/v1/auth/request-access").mock(side_effect=handler)
    resource = SyncAuthResource(SyncHttpClient(base_url=BASE, max_retries=0))
    resource.request_access("test@example.com", True)
