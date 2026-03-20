from __future__ import annotations

from bizverify._client import AsyncHttpClient, SyncHttpClient
from bizverify._errors import (
    AuthenticationError,
    AuthorizationError,
    BizVerifyError,
    ConflictError,
    InsufficientCreditsError,
    InternalError,
    JobFailedError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)
from bizverify._models import (
    Account,
    Address,
    ApiKeyInfo,
    BillingInfo,
    CheckerResponse,
    CheckerResult,
    ConfigResponse,
    CreateKeyResponse,
    DataExport,
    DataExportApiKey,
    DataExportJob,
    DataExportProfile,
    DataExportTransaction,
    EndpointSummary,
    Entity,
    FilingSummary,
    JobStatusResponse,
    JurisdictionInfo,
    JurisdictionSummary,
    JurisdictionsResponse,
    MessageResponse,
    Officer,
    PaginatedSnapshots,
    PurchaseResponse,
    RegisteredAgent,
    RequestAccessResponse,
    ResponseMeta,
    SearchResponse,
    SearchResult,
    UsageEntry,
    UsageStats,
    User,
    VerifyAccessResponse,
    VerifyResponse,
)
from bizverify.resources._account import AsyncAccountResource, SyncAccountResource
from bizverify.resources._auth import AsyncAuthResource, SyncAuthResource
from bizverify.resources._billing import AsyncBillingResource, SyncBillingResource
from bizverify.resources._checker import AsyncCheckerResource, SyncCheckerResource
from bizverify.resources._config import AsyncConfigResource, SyncConfigResource
from bizverify.resources._entities import AsyncEntitiesResource, SyncEntitiesResource
from bizverify.resources._search import AsyncSearchResource, SyncSearchResource
from bizverify.resources._verification import AsyncVerificationResource, SyncVerificationResource


class BizVerify:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        max_retries: int | None = None,
        timeout: float | None = None,
    ) -> None:
        self._client = SyncHttpClient(
            base_url=base_url, api_key=api_key,
            max_retries=max_retries, timeout=timeout,
        )
        self.auth = SyncAuthResource(self._client)
        self.verification = SyncVerificationResource(self._client)
        self.entities = SyncEntitiesResource(self._client)
        self.search = SyncSearchResource(self._client)
        self.account = SyncAccountResource(self._client)
        self.billing = SyncBillingResource(self._client)
        self.checker = SyncCheckerResource(self._client)
        self.config = SyncConfigResource(self._client)

    @property
    def last_response_meta(self) -> ResponseMeta | None:
        return self._client.last_response_meta

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> BizVerify:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncBizVerify:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        max_retries: int | None = None,
        timeout: float | None = None,
    ) -> None:
        self._client = AsyncHttpClient(
            base_url=base_url, api_key=api_key,
            max_retries=max_retries, timeout=timeout,
        )
        self.auth = AsyncAuthResource(self._client)
        self.verification = AsyncVerificationResource(self._client)
        self.entities = AsyncEntitiesResource(self._client)
        self.search = AsyncSearchResource(self._client)
        self.account = AsyncAccountResource(self._client)
        self.billing = AsyncBillingResource(self._client)
        self.checker = AsyncCheckerResource(self._client)
        self.config = AsyncConfigResource(self._client)

    @property
    def last_response_meta(self) -> ResponseMeta | None:
        return self._client.last_response_meta

    async def close(self) -> None:
        await self._client.close()

    async def __aenter__(self) -> AsyncBizVerify:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()


__all__ = [
    "BizVerify",
    "AsyncBizVerify",
    "BizVerifyError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "NotFoundError",
    "InsufficientCreditsError",
    "RateLimitError",
    "ConflictError",
    "InternalError",
    "TimeoutError",
    "JobFailedError",
    "Address",
    "RegisteredAgent",
    "Officer",
    "FilingSummary",
    "User",
    "RequestAccessResponse",
    "VerifyAccessResponse",
    "ResponseMeta",
    "ConfigResponse",
    "JurisdictionInfo",
    "JurisdictionsResponse",
    "MessageResponse",
    "VerifyResponse",
    "JobStatusResponse",
    "Entity",
    "PaginatedSnapshots",
    "SearchResult",
    "SearchResponse",
    "ApiKeyInfo",
    "Account",
    "UsageEntry",
    "EndpointSummary",
    "JurisdictionSummary",
    "UsageStats",
    "DataExport",
    "DataExportProfile",
    "DataExportApiKey",
    "DataExportTransaction",
    "DataExportJob",
    "CreateKeyResponse",
    "BillingInfo",
    "PurchaseResponse",
    "CheckerResult",
    "CheckerResponse",
]
