from __future__ import annotations

from typing import Any


class BizVerifyError(Exception):
    def __init__(self, message: str, code: str, status_code: int, details: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class AuthenticationError(BizVerifyError):
    def __init__(self, message: str, code: str, details: Any = None) -> None:
        super().__init__(message, code, 401, details)


class AuthorizationError(BizVerifyError):
    def __init__(self, message: str, code: str, details: Any = None) -> None:
        super().__init__(message, code, 403, details)


class ValidationError(BizVerifyError):
    def __init__(self, message: str, code: str, details: Any = None) -> None:
        super().__init__(message, code, 400, details)


class NotFoundError(BizVerifyError):
    def __init__(self, message: str, code: str, details: Any = None) -> None:
        super().__init__(message, code, 404, details)


class InsufficientCreditsError(BizVerifyError):
    def __init__(self, message: str, code: str, details: Any = None) -> None:
        super().__init__(message, code, 402, details)


class RateLimitError(BizVerifyError):
    def __init__(self, message: str, code: str, retry_after: int | None = None, details: Any = None) -> None:
        super().__init__(message, code, 429, details)
        self.retry_after = retry_after


class ConflictError(BizVerifyError):
    def __init__(self, message: str, code: str, details: Any = None) -> None:
        super().__init__(message, code, 409, details)


class InternalError(BizVerifyError):
    def __init__(self, message: str, code: str, status_code: int = 500, details: Any = None) -> None:
        super().__init__(message, code, status_code, details)


class TimeoutError(BizVerifyError):
    def __init__(self, message: str) -> None:
        super().__init__(message, "TIMEOUT", 0)


class JobFailedError(BizVerifyError):
    def __init__(self, message: str, job_id: str, details: Any = None) -> None:
        super().__init__(message, "JOB_FAILED", 0, details)
        self.job_id = job_id


def parse_error_response(status_code: int, body: dict[str, Any], headers: Any) -> BizVerifyError:
    error_data = body.get("error", {})
    code = error_data.get("code", "UNKNOWN")
    message = error_data.get("message", "Unknown error")
    details = error_data.get("details")

    if status_code in (400, 422):
        return ValidationError(message, code, details)
    if status_code == 401:
        return AuthenticationError(message, code, details)
    if status_code == 402:
        return InsufficientCreditsError(message, code, details)
    if status_code == 403:
        return AuthorizationError(message, code, details)
    if status_code == 404:
        return NotFoundError(message, code, details)
    if status_code == 409:
        return ConflictError(message, code, details)
    if status_code == 429:
        retry_after = None
        ra = headers.get("retry-after") if hasattr(headers, "get") else None
        if ra is not None:
            try:
                retry_after = int(ra)
            except (ValueError, TypeError):
                pass
        return RateLimitError(message, code, retry_after, details)
    if status_code >= 500:
        return InternalError(message, code, status_code, details)
    return BizVerifyError(message, code, status_code, details)
