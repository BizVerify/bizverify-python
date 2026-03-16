from __future__ import annotations

import httpx

from bizverify.resources._entities import SyncEntitiesResource
from tests.fixtures import ENTITY_RESPONSE, HISTORY_RESPONSE


def test_get_entity(mock_api, sync_client):
    mock_api.get("/v1/entity/ent_123").mock(return_value=httpx.Response(200, json=ENTITY_RESPONSE))
    resource = SyncEntitiesResource(sync_client)
    entity = resource.get("ent_123")
    assert entity.id == "ent_123"
    assert entity.entity_name == "Acme Inc"
    assert entity.entity_type == "corporation"
    assert entity.registered_agent is not None
    assert entity.registered_agent.name == "Agent Corp"


def test_history_no_params(mock_api, sync_client):
    mock_api.get("/v1/entity/ent_123/history").mock(return_value=httpx.Response(200, json=HISTORY_RESPONSE))
    resource = SyncEntitiesResource(sync_client)
    resp = resource.history("ent_123")
    assert resp.total == 1
    assert len(resp.snapshots) == 1


def test_history_with_params(mock_api, sync_client):
    def handler(request):
        assert "limit=10" in str(request.url)
        assert "offset=5" in str(request.url)
        return httpx.Response(200, json=HISTORY_RESPONSE)

    mock_api.get("/v1/entity/ent_123/history").mock(side_effect=handler)
    resource = SyncEntitiesResource(sync_client)
    resource.history("ent_123", limit=10, offset=5)
