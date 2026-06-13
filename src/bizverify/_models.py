from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

VerificationLevel = Literal["quick", "deep"]


@dataclass(frozen=True)
class Address:
    line1: str
    line2: str | None
    city: str
    state: str | None
    postal_code: str | None
    country: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Address:
        return cls(
            line1=data["line1"],
            line2=data.get("line2"),
            city=data["city"],
            state=data.get("state"),
            postal_code=data.get("postal_code"),
            country=data["country"],
        )


@dataclass(frozen=True)
class RegisteredAgent:
    name: str
    address: Address | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RegisteredAgent:
        addr = Address.from_dict(data["address"]) if data.get("address") else None
        return cls(name=data["name"], address=addr)


@dataclass(frozen=True)
class Officer:
    name: str
    title: str
    address: Address | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Officer:
        addr = Address.from_dict(data["address"]) if data.get("address") else None
        return cls(name=data["name"], title=data["title"], address=addr)


@dataclass(frozen=True)
class FilingSummary:
    date: str
    type: str
    description: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FilingSummary:
        return cls(date=data["date"], type=data["type"], description=data.get("description"))


@dataclass(frozen=True)
class User:
    id: str
    email: str
    email_verified: bool
    plan: str
    credit_balance: int
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls(
            id=data["id"],
            email=data["email"],
            email_verified=data["email_verified"],
            plan=data["plan"],
            credit_balance=data["credit_balance"],
            created_at=data["created_at"],
        )


@dataclass(frozen=True)
class RequestAccessResponse:
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RequestAccessResponse:
        return cls(message=data["message"])


@dataclass(frozen=True)
class VerifyAccessResponse:
    api_key: str
    key_id: str
    label: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VerifyAccessResponse:
        return cls(api_key=data["api_key"], key_id=data["key_id"], label=data["label"])


@dataclass(frozen=True)
class ResponseMeta:
    credits_remaining: int | None
    credits_charged: int | None
    rate_limit_limit: int | None
    rate_limit_remaining: int | None
    rate_limit_reset: int | None


@dataclass(frozen=True)
class ConfigResponse:
    jurisdictions: dict[str, Any]
    checker: dict[str, Any]
    pricing: dict[str, Any]
    features: dict[str, Any]
    rate_limits: dict[str, Any]
    status: dict[str, Any]
    legal: dict[str, Any]
    docs: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConfigResponse:
        return cls(
            jurisdictions=data["jurisdictions"],
            checker=data["checker"],
            pricing=data["pricing"],
            features=data["features"],
            rate_limits=data["rateLimits"],
            status=data["status"],
            legal=data["legal"],
            docs=data["docs"],
        )


@dataclass(frozen=True)
class JurisdictionInfo:
    code: str
    name: str
    features: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JurisdictionInfo:
        return cls(code=data["code"], name=data["name"], features=data["features"])


@dataclass(frozen=True)
class JurisdictionsResponse:
    jurisdictions: list[JurisdictionInfo]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JurisdictionsResponse:
        return cls(jurisdictions=[JurisdictionInfo.from_dict(j) for j in data["jurisdictions"]])


@dataclass(frozen=True)
class MessageResponse:
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MessageResponse:
        return cls(message=data["message"])


@dataclass(frozen=True)
class VerificationReason:
    code: str
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VerificationReason:
        return cls(code=data["code"], message=data["message"])


@dataclass(frozen=True)
class VerifyResponse:
    status: str
    data: Any
    job_id: str | None
    entity_id: str | None
    cached: bool
    credits_charged: int
    verification_level: str | None = None
    full_verification_available: bool | None = None
    reason: VerificationReason | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VerifyResponse:
        return cls(
            status=data["status"],
            data=data.get("data"),
            job_id=data.get("job_id"),
            entity_id=data.get("entity_id"),
            cached=data["cached"],
            credits_charged=data["credits_charged"],
            verification_level=data.get("verification_level"),
            full_verification_available=data.get("full_verification_available"),
            reason=VerificationReason.from_dict(data["reason"]) if data.get("reason") else None,
        )


@dataclass(frozen=True)
class JobStatusResponse:
    id: str
    status: str
    jurisdiction: str
    query: str
    verification_level: str
    credits_charged: int
    result: Any
    error: str | None
    created_at: str
    completed_at: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JobStatusResponse:
        return cls(
            id=data["id"],
            status=data["status"],
            jurisdiction=data["jurisdiction"],
            query=data["query"],
            verification_level=data["verification_level"],
            credits_charged=data["credits_charged"],
            result=data.get("result"),
            error=data.get("error"),
            created_at=data["created_at"],
            completed_at=data.get("completed_at"),
        )


@dataclass(frozen=True)
class Entity:
    id: str
    entity_name: str
    jurisdiction: str
    entity_type: str
    status: str
    jurisdiction_id: str | None
    good_standing: bool | None
    formation_date: str | None
    registered_agent: RegisteredAgent | None
    officers: list[Officer]
    principal_address: Address | None
    filing_history_summary: list[FilingSummary]
    created_at: str
    updated_at: str
    last_verified_at: str | None = None
    snapshots: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Entity:
        ra = RegisteredAgent.from_dict(data["registered_agent"]) if data.get("registered_agent") else None
        officers = [Officer.from_dict(o) for o in data.get("officers", [])]
        addr = Address.from_dict(data["principal_address"]) if data.get("principal_address") else None
        filings = [FilingSummary.from_dict(f) for f in data.get("filing_history_summary", [])]
        return cls(
            id=data["id"],
            entity_name=data["entity_name"],
            jurisdiction=data["jurisdiction"],
            entity_type=data["entity_type"],
            status=data["status"],
            jurisdiction_id=data.get("jurisdiction_id"),
            good_standing=data.get("good_standing"),
            formation_date=data.get("formation_date"),
            registered_agent=ra,
            officers=officers,
            principal_address=addr,
            filing_history_summary=filings,
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            last_verified_at=data.get("last_verified_at"),
            snapshots=data.get("snapshots"),
        )


@dataclass(frozen=True)
class PaginatedSnapshots:
    snapshots: list[Any]
    total: int
    limit: int
    offset: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaginatedSnapshots:
        return cls(
            snapshots=data.get("snapshots", []),
            total=data["total"],
            limit=data["limit"],
            offset=data["offset"],
        )


@dataclass(frozen=True)
class SearchResult:
    entity_name: str
    jurisdiction: str
    entity_type: str
    status: str
    jurisdiction_id: str | None
    confidence: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SearchResult:
        return cls(
            entity_name=data["entity_name"],
            jurisdiction=data["jurisdiction"],
            entity_type=data["entity_type"],
            status=data["status"],
            jurisdiction_id=data.get("jurisdiction_id"),
            confidence=data["confidence"],
        )


@dataclass(frozen=True)
class SearchResponse:
    results: list[SearchResult]
    total: int
    limit: int
    offset: int
    jurisdictions_searched: list[str]
    jurisdictions_failed: list[str]
    credits_charged: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SearchResponse:
        return cls(
            results=[SearchResult.from_dict(r) for r in data.get("results", [])],
            total=data["total"],
            limit=data["limit"],
            offset=data["offset"],
            jurisdictions_searched=data.get("jurisdictions_searched", []),
            jurisdictions_failed=data.get("jurisdictions_failed", []),
            credits_charged=data["credits_charged"],
        )


@dataclass(frozen=True)
class ApiKeyInfo:
    id: str
    label: str
    prefix: str
    rate_limit: int
    is_active: bool
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ApiKeyInfo:
        return cls(
            id=data["id"],
            label=data["label"],
            prefix=data["prefix"],
            rate_limit=data["rate_limit"],
            is_active=data["is_active"],
            created_at=data["created_at"],
        )


@dataclass(frozen=True)
class Account:
    id: str
    email: str
    email_verified: bool
    plan: str
    credit_balance: int
    api_keys: list[ApiKeyInfo]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Account:
        return cls(
            id=data["id"],
            email=data["email"],
            email_verified=data["email_verified"],
            plan=data["plan"],
            credit_balance=data["credit_balance"],
            api_keys=[ApiKeyInfo.from_dict(k) for k in data.get("api_keys", [])],
            created_at=data["created_at"],
        )


@dataclass(frozen=True)
class UsageEntry:
    date: str
    endpoint: str
    jurisdiction: str | None
    request_count: int
    credits_used: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UsageEntry:
        return cls(
            date=data["date"],
            endpoint=data["endpoint"],
            jurisdiction=data.get("jurisdiction"),
            request_count=data["request_count"],
            credits_used=data["credits_used"],
        )


@dataclass(frozen=True)
class EndpointSummary:
    endpoint: str
    total_requests: int
    total_credits: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EndpointSummary:
        return cls(
            endpoint=data["endpoint"],
            total_requests=data["total_requests"],
            total_credits=data["total_credits"],
        )


@dataclass(frozen=True)
class JurisdictionSummary:
    jurisdiction: str
    total_requests: int
    total_credits: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JurisdictionSummary:
        return cls(
            jurisdiction=data["jurisdiction"],
            total_requests=data["total_requests"],
            total_credits=data["total_credits"],
        )


@dataclass(frozen=True)
class UsageStats:
    period_days: int
    daily: list[UsageEntry]
    by_endpoint: list[EndpointSummary]
    by_jurisdiction: list[JurisdictionSummary]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UsageStats:
        return cls(
            period_days=data["period_days"],
            daily=[UsageEntry.from_dict(e) for e in data.get("daily", [])],
            by_endpoint=[EndpointSummary.from_dict(e) for e in data.get("by_endpoint", [])],
            by_jurisdiction=[JurisdictionSummary.from_dict(e) for e in data.get("by_jurisdiction", [])],
        )


@dataclass(frozen=True)
class DataExportProfile:
    id: str
    email: str
    email_verified: bool
    plan: str
    credit_balance: int
    terms_accepted_at: str | None
    terms_version: str | None
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DataExportProfile:
        return cls(
            id=data["id"],
            email=data["email"],
            email_verified=data["email_verified"],
            plan=data["plan"],
            credit_balance=data["credit_balance"],
            terms_accepted_at=data.get("terms_accepted_at"),
            terms_version=data.get("terms_version"),
            created_at=data["created_at"],
        )


@dataclass(frozen=True)
class DataExportApiKey:
    id: str
    label: str
    prefix: str
    rate_limit: int
    is_active: bool
    created_at: str
    revoked_at: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DataExportApiKey:
        return cls(
            id=data["id"],
            label=data["label"],
            prefix=data["prefix"],
            rate_limit=data["rate_limit"],
            is_active=data["is_active"],
            created_at=data["created_at"],
            revoked_at=data.get("revoked_at"),
        )


@dataclass(frozen=True)
class DataExportTransaction:
    id: str
    amount: int
    balance_after: int
    type: str
    description: str
    reference_id: str | None
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DataExportTransaction:
        return cls(
            id=data["id"],
            amount=data["amount"],
            balance_after=data["balance_after"],
            type=data["type"],
            description=data["description"],
            reference_id=data.get("reference_id"),
            created_at=data["created_at"],
        )


@dataclass(frozen=True)
class DataExportJob:
    id: str
    jurisdiction: str
    query: str
    status: str
    credits_charged: int
    created_at: str
    completed_at: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DataExportJob:
        return cls(
            id=data["id"],
            jurisdiction=data["jurisdiction"],
            query=data["query"],
            status=data["status"],
            credits_charged=data["credits_charged"],
            created_at=data["created_at"],
            completed_at=data.get("completed_at"),
        )


@dataclass(frozen=True)
class DataExport:
    profile: DataExportProfile
    api_keys: list[DataExportApiKey]
    credit_transactions: list[DataExportTransaction]
    verification_jobs: list[DataExportJob]
    usage_stats: list[UsageEntry]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DataExport:
        return cls(
            profile=DataExportProfile.from_dict(data["profile"]),
            api_keys=[DataExportApiKey.from_dict(k) for k in data.get("api_keys", [])],
            credit_transactions=[DataExportTransaction.from_dict(t) for t in data.get("credit_transactions", [])],
            verification_jobs=[DataExportJob.from_dict(j) for j in data.get("verification_jobs", [])],
            usage_stats=[UsageEntry.from_dict(e) for e in data.get("usage_stats", [])],
        )


@dataclass(frozen=True)
class CreateKeyResponse:
    id: str
    key: str
    prefix: str
    label: str
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CreateKeyResponse:
        return cls(id=data["id"], key=data["key"], prefix=data["prefix"], label=data["label"], message=data["message"])


@dataclass(frozen=True)
class BillingInfo:
    balance: int
    packages: Any
    transactions: Any

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BillingInfo:
        return cls(balance=data["balance"], packages=data.get("packages"), transactions=data.get("transactions"))


@dataclass(frozen=True)
class PurchaseResponse:
    session_id: str
    url: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PurchaseResponse:
        return cls(session_id=data["session_id"], url=data["url"])


@dataclass(frozen=True)
class CheckerResult:
    entity_name: str
    entity_type: str
    status: str
    jurisdiction: str
    confidence: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CheckerResult:
        return cls(
            entity_name=data["entity_name"],
            entity_type=data["entity_type"],
            status=data["status"],
            jurisdiction=data["jurisdiction"],
            confidence=data["confidence"],
        )


@dataclass(frozen=True)
class CheckerResponse:
    results: list[CheckerResult]
    query: str
    jurisdiction: str
    total: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CheckerResponse:
        return cls(
            results=[CheckerResult.from_dict(r) for r in data.get("results", [])],
            query=data["query"],
            jurisdiction=data["jurisdiction"],
            total=data["total"],
        )
