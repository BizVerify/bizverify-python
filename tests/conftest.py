from __future__ import annotations

import pytest
import respx

from bizverify._client import AsyncHttpClient, SyncHttpClient

BASE = "https://api.bizverify.co"


@pytest.fixture
def mock_api():
    with respx.mock(base_url=BASE) as respx_mock:
        yield respx_mock


@pytest.fixture
def sync_client():
    client = SyncHttpClient(base_url=BASE, api_key="test-key", token="test-token", max_retries=0)
    yield client
    client.close()


@pytest.fixture
def async_client():
    return AsyncHttpClient(base_url=BASE, api_key="test-key", token="test-token", max_retries=0)
