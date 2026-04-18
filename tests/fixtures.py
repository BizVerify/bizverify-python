from __future__ import annotations

from typing import Any

REQUEST_ACCESS_RESPONSE: dict[str, Any] = {"message": "Verification code sent to test@example.com"}

VERIFY_ACCESS_RESPONSE: dict[str, Any] = {
    "api_key": "bv_live_abc123def456",
    "key_id": "key_001",
    "label": "key-1710000000",
}

MESSAGE_RESPONSE: dict[str, Any] = {"message": "Success"}

VERIFY_RESPONSE_SYNC: dict[str, Any] = {
    "status": "completed",
    "data": {"exists": True},
    "entity_id": "ent_123",
    "cached": True,
    "credits_charged": 1,
}

VERIFY_RESPONSE_ASYNC: dict[str, Any] = {
    "status": "pending",
    "job_id": "job_456",
    "cached": False,
    "credits_charged": 15,
}

JOB_STATUS_PENDING: dict[str, Any] = {
    "id": "job_456",
    "status": "pending",
    "jurisdiction": "us-fl",
    "query": "Acme Inc",
    "verification_level": "deep",
    "credits_charged": 15,
    "created_at": "2026-01-01T00:00:00.000Z",
    "completed_at": None,
}

JOB_STATUS_COMPLETED: dict[str, Any] = {
    "id": "job_456",
    "status": "completed",
    "jurisdiction": "us-fl",
    "query": "Acme Inc",
    "verification_level": "deep",
    "credits_charged": 15,
    "result": {"exists": True},
    "created_at": "2026-01-01T00:00:00.000Z",
    "completed_at": "2026-01-01T00:01:00.000Z",
}

JOB_STATUS_FAILED: dict[str, Any] = {
    "id": "job_456",
    "status": "failed",
    "jurisdiction": "us-fl",
    "query": "Acme Inc",
    "verification_level": "deep",
    "credits_charged": 15,
    "error": "Data source timeout",
    "created_at": "2026-01-01T00:00:00.000Z",
    "completed_at": "2026-01-01T00:01:00.000Z",
}

ENTITY_RESPONSE: dict[str, Any] = {
    "id": "ent_123",
    "entity_name": "Acme Inc",
    "jurisdiction": "us-fl",
    "entity_type": "corporation",
    "status": "active",
    "jurisdiction_id": "FL12345",
    "good_standing": True,
    "formation_date": "2020-01-15",
    "registered_agent": {"name": "Agent Corp", "address": None},
    "officers": [],
    "principal_address": None,
    "filing_history_summary": [],
    "created_at": "2026-01-01T00:00:00.000Z",
    "updated_at": "2026-01-01T00:00:00.000Z",
}

HISTORY_RESPONSE: dict[str, Any] = {
    "snapshots": [{"id": "snap_1", "data": {}}],
    "total": 1,
    "limit": 50,
    "offset": 0,
}

SEARCH_RESPONSE: dict[str, Any] = {
    "results": [
        {
            "entity_name": "Acme Inc",
            "jurisdiction": "us-fl",
            "entity_type": "corporation",
            "status": "active",
            "jurisdiction_id": "FL12345",
            "confidence": 0.95,
        },
    ],
    "total": 1,
    "limit": 50,
    "offset": 0,
    "jurisdictions_searched": ["us-fl"],
    "jurisdictions_failed": [],
    "credits_charged": 2,
}

ACCOUNT_RESPONSE: dict[str, Any] = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "email_verified": True,
    "plan": "free",
    "credit_balance": 100,
    "api_keys": [],
    "created_at": "2026-01-01T00:00:00.000Z",
}

USAGE_RESPONSE: dict[str, Any] = {
    "period_days": 30,
    "daily": [],
    "by_endpoint": [],
    "by_jurisdiction": [],
}

DATA_EXPORT_RESPONSE: dict[str, Any] = {
    "profile": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "test@example.com",
        "email_verified": True,
        "plan": "free",
        "credit_balance": 100,
        "terms_accepted_at": None,
        "terms_version": None,
        "created_at": "2026-01-01T00:00:00.000Z",
    },
    "api_keys": [],
    "credit_transactions": [],
    "verification_jobs": [],
    "usage_stats": [],
}

CREATE_KEY_RESPONSE: dict[str, Any] = {
    "id": "key_123",
    "key": "bv_live_newkey",
    "prefix": "bv_live_new",
    "label": "My Key",
    "message": "Store this API key securely. It will not be shown again.",
}

BILLING_RESPONSE: dict[str, Any] = {
    "balance": 100,
    "packages": [],
    "transactions": [],
}

PURCHASE_RESPONSE: dict[str, Any] = {
    "session_id": "cs_test_123",
    "url": "https://checkout.stripe.com/session/cs_test_123",
}

CHECKER_RESPONSE: dict[str, Any] = {
    "results": [
        {
            "entity_name": "Acme Inc",
            "entity_type": "corporation",
            "status": "active",
            "jurisdiction": "us-fl",
            "confidence": 0.9,
        },
    ],
    "query": "Acme",
    "jurisdiction": "us-fl",
    "total": 1,
}

CONFIG_RESPONSE: dict[str, Any] = {
    "jurisdictions": {
        "stats": {"totalJurisdictions": 61, "usStates": 50, "countries": 11},
        "supported": {"us": ["us-fl"], "international": ["ee"], "comingSoon": []},
    },
    "checker": {"jurisdictions": [{"label": "Florida", "code": "us-fl"}]},
    "pricing": {
        "creditCosts": {"verify": 15, "search": 2},
        "freeTier": {"credits": 50, "replenish": "never", "rateLimit": "10/min"},
        "packages": [],
    },
    "features": {"verification": True, "search": True},
    "rateLimits": {"default": 60},
    "status": {"api": "operational", "lastUpdated": "2026-03-20T00:00:00Z"},
    "legal": {"terms_url": "https://bizverify.co/terms", "privacy_url": "https://bizverify.co/privacy", "version": "1.0"},
    "docs": {"openapi": "/v1/openapi.json", "interactive": "/docs"},
}

JURISDICTIONS_RESPONSE: dict[str, Any] = {
    "jurisdictions": [
        {"code": "us-fl", "name": "Florida", "features": {"search": True, "verify": True}},
    ]
}


def error_response(code: str, message: str) -> dict[str, Any]:
    return {"error": {"code": code, "message": message}}
