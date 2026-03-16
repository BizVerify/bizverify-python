from __future__ import annotations

import httpx

from bizverify.resources._account import SyncAccountResource
from tests.fixtures import (
    ACCOUNT_RESPONSE,
    CREATE_KEY_RESPONSE,
    DATA_EXPORT_RESPONSE,
    MESSAGE_RESPONSE,
    USAGE_RESPONSE,
)


def test_get_account(mock_api, sync_client):
    mock_api.get("/v1/account").mock(return_value=httpx.Response(200, json=ACCOUNT_RESPONSE))
    resource = SyncAccountResource(sync_client)
    account = resource.get()
    assert account.id == "550e8400-e29b-41d4-a716-446655440000"
    assert account.credit_balance == 100


def test_usage_no_days(mock_api, sync_client):
    mock_api.get("/v1/account/usage").mock(return_value=httpx.Response(200, json=USAGE_RESPONSE))
    resource = SyncAccountResource(sync_client)
    usage = resource.usage()
    assert usage.period_days == 30


def test_usage_with_days(mock_api, sync_client):
    def handler(request):
        assert "days=7" in str(request.url)
        return httpx.Response(200, json=USAGE_RESPONSE)

    mock_api.get("/v1/account/usage").mock(side_effect=handler)
    resource = SyncAccountResource(sync_client)
    resource.usage(days=7)


def test_data_export(mock_api, sync_client):
    mock_api.get("/v1/account/data-export").mock(return_value=httpx.Response(200, json=DATA_EXPORT_RESPONSE))
    resource = SyncAccountResource(sync_client)
    export = resource.data_export()
    assert export.profile.email == "test@example.com"


def test_update_email(mock_api, sync_client):
    mock_api.patch("/v1/account").mock(return_value=httpx.Response(200, json=MESSAGE_RESPONSE))
    resource = SyncAccountResource(sync_client)
    resp = resource.update_email("new@example.com")
    assert resp.message == "Success"


def test_update_password(mock_api, sync_client):
    mock_api.put("/v1/account/password").mock(return_value=httpx.Response(200, json=MESSAGE_RESPONSE))
    resource = SyncAccountResource(sync_client)
    resp = resource.update_password("oldpass", "newpass")
    assert resp.message == "Success"


def test_delete_account(mock_api, sync_client):
    mock_api.delete("/v1/account").mock(return_value=httpx.Response(204))
    resource = SyncAccountResource(sync_client)
    result = resource.delete("mypassword")
    assert result is None


def test_create_key(mock_api, sync_client):
    mock_api.post("/v1/account/keys").mock(return_value=httpx.Response(200, json=CREATE_KEY_RESPONSE))
    resource = SyncAccountResource(sync_client)
    resp = resource.create_key("My Key")
    assert resp.key == "bv_live_newkey"
    assert resp.label == "My Key"


def test_revoke_key(mock_api, sync_client):
    mock_api.delete("/v1/account/keys/key_123").mock(return_value=httpx.Response(204))
    resource = SyncAccountResource(sync_client)
    result = resource.revoke_key("key_123")
    assert result is None


def test_account_uses_jwt_auth(mock_api, sync_client):
    def handler(request):
        assert request.headers.get("Authorization") == "Bearer test-token"
        return httpx.Response(200, json=ACCOUNT_RESPONSE)

    mock_api.get("/v1/account").mock(side_effect=handler)
    resource = SyncAccountResource(sync_client)
    resource.get()
