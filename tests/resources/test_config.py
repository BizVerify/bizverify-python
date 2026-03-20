from __future__ import annotations

import httpx

from bizverify._client import SyncHttpClient
from bizverify.resources._config import SyncConfigResource
from tests.fixtures import CONFIG_RESPONSE, JURISDICTIONS_RESPONSE

BASE = "https://api.bizverify.co"


def test_get_config(mock_api, sync_client):
    mock_api.get("/v1/config").mock(return_value=httpx.Response(200, json=CONFIG_RESPONSE))
    resource = SyncConfigResource(sync_client)
    resp = resource.get()
    assert resp.jurisdictions["stats"]["totalJurisdictions"] == 61
    assert resp.features["verification"] is True
    assert resp.rate_limits["default"] == 60
    assert resp.legal["version"] == "1.0"
    assert resp.docs["interactive"] == "/docs"


def test_get_jurisdictions(mock_api, sync_client):
    mock_api.get("/v1/jurisdictions").mock(return_value=httpx.Response(200, json=JURISDICTIONS_RESPONSE))
    resource = SyncConfigResource(sync_client)
    resp = resource.jurisdictions()
    assert len(resp.jurisdictions) == 1
    assert resp.jurisdictions[0].code == "us-fl"
    assert resp.jurisdictions[0].name == "Florida"
    assert resp.jurisdictions[0].features["search"] is True


def test_config_no_auth_header(mock_api, sync_client):
    def handler(request):
        assert "X-API-Key" not in request.headers
        assert "Authorization" not in request.headers
        return httpx.Response(200, json=CONFIG_RESPONSE)

    mock_api.get("/v1/config").mock(side_effect=handler)
    resource = SyncConfigResource(SyncHttpClient(base_url=BASE, max_retries=0))
    resource.get()


def test_jurisdictions_no_auth_header(mock_api, sync_client):
    def handler(request):
        assert "X-API-Key" not in request.headers
        assert "Authorization" not in request.headers
        return httpx.Response(200, json=JURISDICTIONS_RESPONSE)

    mock_api.get("/v1/jurisdictions").mock(side_effect=handler)
    resource = SyncConfigResource(SyncHttpClient(base_url=BASE, max_retries=0))
    resource.jurisdictions()
