from __future__ import annotations

import httpx

from bizverify.resources._checker import SyncCheckerResource
from tests.fixtures import CHECKER_RESPONSE


def test_check(mock_api, sync_client):
    mock_api.post("/v1/checker").mock(return_value=httpx.Response(200, json=CHECKER_RESPONSE))
    resource = SyncCheckerResource(sync_client)
    resp = resource.check("Acme", "us-fl")
    assert resp.total == 1
    assert resp.results[0].entity_name == "Acme Inc"
    assert resp.results[0].confidence == 0.9


def test_checker_no_auth(mock_api, sync_client):
    def handler(request):
        assert "X-API-Key" not in request.headers or request.headers.get("X-API-Key") == ""
        assert "Authorization" not in request.headers or request.headers.get("Authorization") == ""
        return httpx.Response(200, json=CHECKER_RESPONSE)

    mock_api.post("/v1/checker").mock(side_effect=handler)
    from bizverify._client import SyncHttpClient

    client = SyncHttpClient(base_url="https://api.bizverify.co", max_retries=0)
    resource = SyncCheckerResource(client)
    resource.check("Acme", "us-fl")
    client.close()
