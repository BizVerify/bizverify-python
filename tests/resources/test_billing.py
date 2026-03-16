from __future__ import annotations

import httpx

from bizverify.resources._billing import SyncBillingResource
from tests.fixtures import BILLING_RESPONSE, PURCHASE_RESPONSE


def test_get_billing(mock_api, sync_client):
    mock_api.get("/v1/billing").mock(return_value=httpx.Response(200, json=BILLING_RESPONSE))
    resource = SyncBillingResource(sync_client)
    resp = resource.get()
    assert resp.balance == 100


def test_get_billing_with_params(mock_api, sync_client):
    def handler(request):
        assert "limit=10" in str(request.url)
        assert "offset=5" in str(request.url)
        return httpx.Response(200, json=BILLING_RESPONSE)

    mock_api.get("/v1/billing").mock(side_effect=handler)
    resource = SyncBillingResource(sync_client)
    resource.get(limit=10, offset=5)


def test_purchase(mock_api, sync_client):
    mock_api.post("/v1/billing/purchase").mock(return_value=httpx.Response(200, json=PURCHASE_RESPONSE))
    resource = SyncBillingResource(sync_client)
    resp = resource.purchase("pkg_100")
    assert resp.session_id == "cs_test_123"
    assert "stripe.com" in resp.url
