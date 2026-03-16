from __future__ import annotations

import httpx
import pytest
import respx

from bizverify._client import SyncHttpClient
from bizverify.resources._auth import SyncAuthResource
from tests.fixtures import LOGIN_RESPONSE, MESSAGE_RESPONSE, REGISTER_RESPONSE

BASE = "https://api.bizverify.co"


@pytest.fixture
def auth_resource(mock_api, sync_client):
    return SyncAuthResource(sync_client)


def test_register(mock_api, auth_resource):
    def handler(request):
        body = request.content.decode()
        assert '"email": "test@example.com"' in body or '"email":"test@example.com"' in body
        assert "accept_terms" in body
        return httpx.Response(200, json=REGISTER_RESPONSE)

    mock_api.post("/v1/auth/register").mock(side_effect=handler)
    resp = auth_resource.register("test@example.com", "password123", True)
    assert resp.api_key == "bv_live_abc123def456"
    assert resp.user.email == "test@example.com"


def test_login_sets_token(mock_api, sync_client):
    mock_api.post("/v1/auth/login").mock(return_value=httpx.Response(200, json=LOGIN_RESPONSE))
    resource = SyncAuthResource(sync_client)
    resp = resource.login("test@example.com", "password123")
    assert resp.token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
    assert sync_client._token == resp.token


def test_verify_email(mock_api, auth_resource):
    mock_api.post("/v1/auth/verify-email").mock(return_value=httpx.Response(200, json=MESSAGE_RESPONSE))
    resp = auth_resource.verify_email("test@example.com", "123456")
    assert resp.message == "Success"


def test_resend_verification(mock_api, auth_resource):
    mock_api.post("/v1/auth/resend-verification").mock(return_value=httpx.Response(200, json=MESSAGE_RESPONSE))
    resp = auth_resource.resend_verification("test@example.com")
    assert resp.message == "Success"


def test_forgot_password(mock_api, auth_resource):
    mock_api.post("/v1/auth/forgot-password").mock(return_value=httpx.Response(200, json=MESSAGE_RESPONSE))
    resp = auth_resource.forgot_password("test@example.com")
    assert resp.message == "Success"


def test_reset_password(mock_api, auth_resource):
    mock_api.post("/v1/auth/reset-password").mock(return_value=httpx.Response(200, json=MESSAGE_RESPONSE))
    resp = auth_resource.reset_password("test@example.com", "123456", "newpass123")
    assert resp.message == "Success"


def test_register_no_auth_header(mock_api, sync_client):
    def handler(request):
        assert "X-API-Key" not in request.headers
        assert "Authorization" not in request.headers
        return httpx.Response(200, json=REGISTER_RESPONSE)

    mock_api.post("/v1/auth/register").mock(side_effect=handler)
    resource = SyncAuthResource(SyncHttpClient(base_url=BASE, max_retries=0))
    resource.register("test@example.com", "pass", True)
