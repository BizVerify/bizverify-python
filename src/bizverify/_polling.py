from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any, Callable

from bizverify._errors import JobFailedError, TimeoutError
from bizverify._models import JobStatusResponse, VerifyResponse

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient

DEFAULT_POLL_INTERVAL = 2.0
MAX_POLL_INTERVAL = 10.0
DEFAULT_TIMEOUT = 60.0


def poll_until_complete(
    client: SyncHttpClient,
    verify_response: VerifyResponse,
    *,
    poll_interval: float = DEFAULT_POLL_INTERVAL,
    timeout: float = DEFAULT_TIMEOUT,
    on_status_change: Callable[[JobStatusResponse], Any] | None = None,
) -> JobStatusResponse:
    if verify_response.status == "completed" and verify_response.job_id:
        data = client.request("GET", f"/v1/verify/status/{verify_response.job_id}", auth="api_key")
        return JobStatusResponse.from_dict(data)  # type: ignore[arg-type]

    job_id = verify_response.job_id
    if not job_id:
        raise ValueError("No job_id in verify response — cannot poll")

    deadline = time.monotonic() + timeout
    interval = poll_interval
    last_status: str | None = None

    while time.monotonic() < deadline:
        data = client.request("GET", f"/v1/verify/status/{job_id}", auth="api_key")
        status = JobStatusResponse.from_dict(data)  # type: ignore[arg-type]

        if on_status_change and status.status != last_status:
            last_status = status.status
            on_status_change(status)

        if status.status == "completed":
            return status

        if status.status == "failed":
            raise JobFailedError(status.error or "Verification job failed", job_id, status)

        time.sleep(interval)
        interval = min(interval * 1.5, MAX_POLL_INTERVAL)

    raise TimeoutError(f"Polling timed out after {timeout}s for job {job_id}")


async def async_poll_until_complete(
    client: AsyncHttpClient,
    verify_response: VerifyResponse,
    *,
    poll_interval: float = DEFAULT_POLL_INTERVAL,
    timeout: float = DEFAULT_TIMEOUT,
    on_status_change: Callable[[JobStatusResponse], Any] | None = None,
) -> JobStatusResponse:
    if verify_response.status == "completed" and verify_response.job_id:
        data = await client.request("GET", f"/v1/verify/status/{verify_response.job_id}", auth="api_key")
        return JobStatusResponse.from_dict(data)  # type: ignore[arg-type]

    job_id = verify_response.job_id
    if not job_id:
        raise ValueError("No job_id in verify response — cannot poll")

    deadline = time.monotonic() + timeout
    interval = poll_interval
    last_status: str | None = None

    while time.monotonic() < deadline:
        data = await client.request("GET", f"/v1/verify/status/{job_id}", auth="api_key")
        status = JobStatusResponse.from_dict(data)  # type: ignore[arg-type]

        if on_status_change and status.status != last_status:
            last_status = status.status
            on_status_change(status)

        if status.status == "completed":
            return status

        if status.status == "failed":
            raise JobFailedError(status.error or "Verification job failed", job_id, status)

        await asyncio.sleep(interval)
        interval = min(interval * 1.5, MAX_POLL_INTERVAL)

    raise TimeoutError(f"Polling timed out after {timeout}s for job {job_id}")
