from __future__ import annotations

import httpx

from bizverify.resources._verification import SyncVerificationResource
from tests.fixtures import JOB_STATUS_COMPLETED, VERIFY_RESPONSE_ASYNC, VERIFY_RESPONSE_SYNC


def test_verify_sync_response(mock_api, sync_client):
    mock_api.post("/v1/verify").mock(return_value=httpx.Response(200, json=VERIFY_RESPONSE_SYNC))
    resource = SyncVerificationResource(sync_client)
    resp = resource.verify("Acme Inc", "us-fl")
    assert resp.status == "completed"
    assert resp.cached is True
    assert resp.credits_charged == 1


def test_verify_async_response(mock_api, sync_client):
    mock_api.post("/v1/verify").mock(return_value=httpx.Response(200, json=VERIFY_RESPONSE_ASYNC))
    resource = SyncVerificationResource(sync_client)
    resp = resource.verify("Acme Inc", "us-fl")
    assert resp.status == "pending"
    assert resp.job_id == "job_456"


def test_verify_with_optional_params(mock_api, sync_client):
    def handler(request):
        import json
        body = json.loads(request.content)
        assert body["entity_type"] == "llc"
        assert body["verification_level"] == "full"
        assert body["force_refresh"] is True
        assert body["webhook_url"] == "https://example.com/hook"
        return httpx.Response(200, json=VERIFY_RESPONSE_SYNC)

    mock_api.post("/v1/verify").mock(side_effect=handler)
    resource = SyncVerificationResource(sync_client)
    resource.verify(
        "Acme Inc", "us-fl",
        entity_type="llc", verification_level="full",
        force_refresh=True, webhook_url="https://example.com/hook",
    )


def test_get_status(mock_api, sync_client):
    mock_api.get("/v1/verify/status/job_456").mock(return_value=httpx.Response(200, json=JOB_STATUS_COMPLETED))
    resource = SyncVerificationResource(sync_client)
    resp = resource.get_status("job_456")
    assert resp.id == "job_456"
    assert resp.status == "completed"


def test_verify_uses_api_key_auth(mock_api, sync_client):
    def handler(request):
        assert request.headers.get("X-API-Key") == "test-key"
        return httpx.Response(200, json=VERIFY_RESPONSE_SYNC)

    mock_api.post("/v1/verify").mock(side_effect=handler)
    resource = SyncVerificationResource(sync_client)
    resource.verify("Acme", "us-fl")
