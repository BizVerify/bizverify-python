from __future__ import annotations

from typing import TYPE_CHECKING

from bizverify._models import LoginResponse, MessageResponse, RegisterResponse

if TYPE_CHECKING:
    from bizverify._client import AsyncHttpClient, SyncHttpClient


class SyncAuthResource:
    def __init__(self, client: SyncHttpClient) -> None:
        self._client = client

    def register(self, email: str, password: str, accept_terms: bool) -> RegisterResponse:
        data = self._client.request(
            "POST", "/v1/auth/register",
            body={"email": email, "password": password, "accept_terms": accept_terms},
            auth="none",
        )
        return RegisterResponse.from_dict(data)  # type: ignore[arg-type]

    def login(self, email: str, password: str) -> LoginResponse:
        data = self._client.request(
            "POST", "/v1/auth/login",
            body={"email": email, "password": password},
            auth="none",
        )
        resp = LoginResponse.from_dict(data)  # type: ignore[arg-type]
        self._client.set_token(resp.token)
        return resp

    def verify_email(self, email: str, code: str) -> MessageResponse:
        data = self._client.request(
            "POST", "/v1/auth/verify-email",
            body={"email": email, "code": code},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    def resend_verification(self, email: str) -> MessageResponse:
        data = self._client.request(
            "POST", "/v1/auth/resend-verification",
            body={"email": email},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    def forgot_password(self, email: str) -> MessageResponse:
        data = self._client.request(
            "POST", "/v1/auth/forgot-password",
            body={"email": email},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    def reset_password(self, email: str, code: str, new_password: str) -> MessageResponse:
        data = self._client.request(
            "POST", "/v1/auth/reset-password",
            body={"email": email, "code": code, "new_password": new_password},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]


class AsyncAuthResource:
    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def register(self, email: str, password: str, accept_terms: bool) -> RegisterResponse:
        data = await self._client.request(
            "POST", "/v1/auth/register",
            body={"email": email, "password": password, "accept_terms": accept_terms},
            auth="none",
        )
        return RegisterResponse.from_dict(data)  # type: ignore[arg-type]

    async def login(self, email: str, password: str) -> LoginResponse:
        data = await self._client.request(
            "POST", "/v1/auth/login",
            body={"email": email, "password": password},
            auth="none",
        )
        resp = LoginResponse.from_dict(data)  # type: ignore[arg-type]
        self._client.set_token(resp.token)
        return resp

    async def verify_email(self, email: str, code: str) -> MessageResponse:
        data = await self._client.request(
            "POST", "/v1/auth/verify-email",
            body={"email": email, "code": code},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    async def resend_verification(self, email: str) -> MessageResponse:
        data = await self._client.request(
            "POST", "/v1/auth/resend-verification",
            body={"email": email},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    async def forgot_password(self, email: str) -> MessageResponse:
        data = await self._client.request(
            "POST", "/v1/auth/forgot-password",
            body={"email": email},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]

    async def reset_password(self, email: str, code: str, new_password: str) -> MessageResponse:
        data = await self._client.request(
            "POST", "/v1/auth/reset-password",
            body={"email": email, "code": code, "new_password": new_password},
            auth="none",
        )
        return MessageResponse.from_dict(data)  # type: ignore[arg-type]
