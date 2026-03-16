from __future__ import annotations

import httpx
import pytest
import respx

from bizverify._client import SyncHttpClient
from bizverify._errors import JobFailedError, TimeoutError
from bizverify._models import VerifyResponse
from bizverify._polling import poll_until_complete
from tests.fixtures import JOB_STATUS_COMPLETED, JOB_STATUS_FAILED, JOB_STATUS_PENDING

BASE = "https://api.bizverify.co"


def test_poll_already_completed():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/verify/status/job_456").mock(return_value=httpx.Response(200, json=JOB_STATUS_COMPLETED))
        client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
        resp = VerifyResponse(status="completed", data=None, job_id="job_456", entity_id=None, cached=True, credits_charged=1)
        result = poll_until_complete(client, resp, poll_interval=0.01, timeout=1.0)
        assert result.status == "completed"
        assert result.id == "job_456"
        client.close()


def test_poll_pending_to_completed():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            return httpx.Response(200, json=JOB_STATUS_PENDING)
        return httpx.Response(200, json=JOB_STATUS_COMPLETED)

    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/verify/status/job_456").mock(side_effect=handler)
        client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
        resp = VerifyResponse(status="pending", data=None, job_id="job_456", entity_id=None, cached=False, credits_charged=15)
        result = poll_until_complete(client, resp, poll_interval=0.01, timeout=5.0)
        assert result.status == "completed"
        assert call_count == 2
        client.close()


def test_poll_pending_to_failed():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            return httpx.Response(200, json=JOB_STATUS_PENDING)
        return httpx.Response(200, json=JOB_STATUS_FAILED)

    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/verify/status/job_456").mock(side_effect=handler)
        client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
        resp = VerifyResponse(status="pending", data=None, job_id="job_456", entity_id=None, cached=False, credits_charged=15)
        with pytest.raises(JobFailedError) as exc_info:
            poll_until_complete(client, resp, poll_interval=0.01, timeout=5.0)
        assert exc_info.value.job_id == "job_456"
        client.close()


def test_poll_timeout():
    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/verify/status/job_456").mock(return_value=httpx.Response(200, json=JOB_STATUS_PENDING))
        client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
        resp = VerifyResponse(status="pending", data=None, job_id="job_456", entity_id=None, cached=False, credits_charged=15)
        with pytest.raises(TimeoutError):
            poll_until_complete(client, resp, poll_interval=0.01, timeout=0.05)
        client.close()


def test_poll_no_job_id():
    client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
    resp = VerifyResponse(status="pending", data=None, job_id=None, entity_id=None, cached=False, credits_charged=15)
    with pytest.raises(ValueError, match="No job_id"):
        poll_until_complete(client, resp)
    client.close()


def test_poll_status_change_callback():
    call_count = 0
    statuses_seen: list[str] = []

    def handler(request):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return httpx.Response(200, json=JOB_STATUS_PENDING)
        return httpx.Response(200, json=JOB_STATUS_COMPLETED)

    def on_change(status):
        statuses_seen.append(status.status)

    with respx.mock(base_url=BASE) as mock:
        mock.get("/v1/verify/status/job_456").mock(side_effect=handler)
        client = SyncHttpClient(base_url=BASE, api_key="k", max_retries=0)
        resp = VerifyResponse(status="pending", data=None, job_id="job_456", entity_id=None, cached=False, credits_charged=15)
        poll_until_complete(client, resp, poll_interval=0.01, timeout=5.0, on_status_change=on_change)
        assert "pending" in statuses_seen
        assert "completed" in statuses_seen
        client.close()
