from __future__ import annotations

import json

import httpx

from bizverify.resources._search import SyncSearchResource
from tests.fixtures import SEARCH_RESPONSE


def test_find(mock_api, sync_client):
    mock_api.post("/v1/search").mock(return_value=httpx.Response(200, json=SEARCH_RESPONSE))
    resource = SyncSearchResource(sync_client)
    resp = resource.find("Acme Inc", jurisdiction="us-fl")
    assert resp.total == 1
    assert resp.results[0].entity_name == "Acme Inc"
    assert resp.credits_charged == 2


def test_find_with_all_params(mock_api, sync_client):
    def handler(request):
        body = json.loads(request.content)
        assert body["entity_name"] == "Acme"
        assert body["jurisdiction"] == "us-fl"
        assert body["entity_type"] == "llc"
        assert body["limit"] == 10
        assert body["offset"] == 5
        return httpx.Response(200, json=SEARCH_RESPONSE)

    mock_api.post("/v1/search").mock(side_effect=handler)
    resource = SyncSearchResource(sync_client)
    resource.find("Acme", jurisdiction="us-fl", entity_type="llc", limit=10, offset=5)


def test_find_all_single_page(mock_api, sync_client):
    mock_api.post("/v1/search").mock(return_value=httpx.Response(200, json=SEARCH_RESPONSE))
    resource = SyncSearchResource(sync_client)
    results = list(resource.find_all("Acme"))
    assert len(results) == 1
    assert results[0].entity_name == "Acme Inc"


def test_find_all_multi_page(mock_api, sync_client):
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        body = json.loads(request.content)
        if body.get("offset", 0) == 0:
            return httpx.Response(200, json={
                "results": [{"entity_name": "A", "jurisdiction": "us-fl", "entity_type": "llc", "status": "active", "jurisdiction_id": None, "confidence": 0.9}],
                "total": 2, "limit": 50, "offset": 0,
                "jurisdictions_searched": ["us-fl"], "jurisdictions_failed": [], "credits_charged": 2,
            })
        return httpx.Response(200, json={
            "results": [{"entity_name": "B", "jurisdiction": "us-fl", "entity_type": "llc", "status": "active", "jurisdiction_id": None, "confidence": 0.8}],
            "total": 2, "limit": 50, "offset": 1,
            "jurisdictions_searched": ["us-fl"], "jurisdictions_failed": [], "credits_charged": 0,
        })

    mock_api.post("/v1/search").mock(side_effect=handler)
    resource = SyncSearchResource(sync_client)
    results = list(resource.find_all("Acme"))
    assert len(results) == 2
    assert results[0].entity_name == "A"
    assert results[1].entity_name == "B"
    assert call_count == 2


def test_find_all_empty(mock_api, sync_client):
    mock_api.post("/v1/search").mock(return_value=httpx.Response(200, json={
        "results": [], "total": 0, "limit": 50, "offset": 0,
        "jurisdictions_searched": ["us-fl"], "jurisdictions_failed": [], "credits_charged": 2,
    }))
    resource = SyncSearchResource(sync_client)
    results = list(resource.find_all("Nothing"))
    assert len(results) == 0
