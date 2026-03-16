from __future__ import annotations

import pytest

from bizverify._errors import (
    AuthenticationError,
    AuthorizationError,
    BizVerifyError,
    ConflictError,
    InsufficientCreditsError,
    InternalError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    parse_error_response,
)
from tests.fixtures import error_response


class FakeHeaders(dict):
    pass


def test_parse_400():
    err = parse_error_response(400, error_response("VALIDATION_ERROR", "Bad input"), FakeHeaders())
    assert isinstance(err, ValidationError)
    assert err.code == "VALIDATION_ERROR"
    assert err.status_code == 400


def test_parse_401():
    err = parse_error_response(401, error_response("INVALID_API_KEY", "Bad key"), FakeHeaders())
    assert isinstance(err, AuthenticationError)
    assert err.status_code == 401


def test_parse_402():
    err = parse_error_response(402, error_response("INSUFFICIENT_CREDITS", "No credits"), FakeHeaders())
    assert isinstance(err, InsufficientCreditsError)
    assert err.status_code == 402


def test_parse_403():
    err = parse_error_response(403, error_response("FORBIDDEN", "Not allowed"), FakeHeaders())
    assert isinstance(err, AuthorizationError)
    assert err.status_code == 403


def test_parse_404():
    err = parse_error_response(404, error_response("NOT_FOUND", "Missing"), FakeHeaders())
    assert isinstance(err, NotFoundError)
    assert err.status_code == 404


def test_parse_409():
    err = parse_error_response(409, error_response("ALREADY_REFUNDED", "Dup"), FakeHeaders())
    assert isinstance(err, ConflictError)
    assert err.status_code == 409


def test_parse_422():
    err = parse_error_response(422, error_response("VALIDATION_ERROR", "Bad data"), FakeHeaders())
    assert isinstance(err, ValidationError)
    assert err.status_code == 400  # ValidationError always has 400


def test_parse_429_with_retry_after():
    headers = FakeHeaders({"retry-after": "30"})
    err = parse_error_response(429, error_response("RATE_LIMIT", "Too fast"), headers)
    assert isinstance(err, RateLimitError)
    assert err.retry_after == 30


def test_parse_429_without_retry_after():
    err = parse_error_response(429, error_response("RATE_LIMIT", "Too fast"), FakeHeaders())
    assert isinstance(err, RateLimitError)
    assert err.retry_after is None


def test_parse_500():
    err = parse_error_response(500, error_response("INTERNAL", "Server error"), FakeHeaders())
    assert isinstance(err, InternalError)
    assert err.status_code == 500


def test_parse_503():
    err = parse_error_response(503, error_response("UNAVAILABLE", "Down"), FakeHeaders())
    assert isinstance(err, InternalError)
    assert err.status_code == 503


def test_parse_unknown_status():
    err = parse_error_response(418, error_response("TEAPOT", "I'm a teapot"), FakeHeaders())
    assert isinstance(err, BizVerifyError)
    assert not isinstance(err, ValidationError)
    assert err.status_code == 418


def test_error_attributes():
    err = parse_error_response(400, {"error": {"code": "TEST", "message": "msg", "details": {"field": "x"}}}, FakeHeaders())
    assert err.message == "msg"
    assert err.code == "TEST"
    assert err.details == {"field": "x"}


def test_error_is_exception():
    err = BizVerifyError("test", "CODE", 400)
    assert isinstance(err, Exception)
    assert str(err) == "test"
