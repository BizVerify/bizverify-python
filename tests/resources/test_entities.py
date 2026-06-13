from __future__ import annotations

import httpx

from bizverify._models import VerifyResponse
from bizverify.resources._entities import SyncEntitiesResource
from tests.fixtures import (
    ENTITY_RESPONSE,
    ENTITY_RESPONSE_FULL,
    HISTORY_RESPONSE,
    VERIFY_RESPONSE_TIERED,
)


def test_get_entity(mock_api, sync_client):
    mock_api.get("/v1/entity/ent_123").mock(return_value=httpx.Response(200, json=ENTITY_RESPONSE))
    resource = SyncEntitiesResource(sync_client)
    entity = resource.get("ent_123")
    assert entity.id == "ent_123"
    assert entity.entity_name == "Acme Inc"
    assert entity.entity_type == "corporation"
    assert entity.registered_agent is not None
    assert entity.registered_agent.name == "Agent Corp"


def test_get_entity_unwrapped_full_shape(mock_api, sync_client):
    """Regression: GET /v1/entity/:id returns the entity unwrapped and deep-shaped.

    Previously the API returned a {entity, snapshots} wrapper, so Entity.from_dict
    raised KeyError: 'id'. The fixed API returns the entity at the top level; this
    test proves entities.get() no longer raises and fully populates the model.
    """
    mock_api.get("/v1/entity/ent_123").mock(return_value=httpx.Response(200, json=ENTITY_RESPONSE_FULL))
    resource = SyncEntitiesResource(sync_client)

    try:
        entity = resource.get("ent_123")
    except KeyError as exc:  # pragma: no cover - explicit regression guard
        raise AssertionError(f"entities.get() raised KeyError on unwrapped shape: {exc}") from exc

    assert entity.id == "550e8400-e29b-41d4-a716-446655440000"
    assert entity.entity_name == "ACME WIDGETS LLC"

    assert entity.registered_agent is not None
    assert entity.registered_agent.name == "JANE AGENT"
    assert entity.registered_agent.address is not None
    assert entity.registered_agent.address.city == "TALLAHASSEE"

    assert len(entity.officers) == 1
    assert entity.officers[0].title == "Manager"

    assert entity.principal_address is not None
    assert entity.principal_address.line1 == "200 COMMERCE BLVD"

    assert len(entity.filing_history_summary) == 1

    assert entity.last_verified_at == "2026-06-13T10:30:00.000Z"
    assert entity.snapshots == 3

    assert entity.created_at == "2024-01-05T08:00:00.000Z"
    assert entity.updated_at == "2026-06-13T10:30:00.000Z"


def test_verify_response_tier_fields():
    """Divergence G: VerifyResponse carries verification-tier fields when present."""
    resp = VerifyResponse.from_dict(VERIFY_RESPONSE_TIERED)
    assert resp.verification_level == "quick"
    assert resp.full_verification_available is True
    assert resp.reason is not None
    assert resp.reason.code == "QUICK_MATCH"
    assert resp.reason.message == "Matched on name and jurisdiction"


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
