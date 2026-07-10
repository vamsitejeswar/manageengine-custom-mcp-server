"""Async httpx client — injects Zoho token into ManageEngine calls.

Token priority:
  1. Per-request context var (Bearer token from Gemini, if present)
  2. Server-managed token (auto-refreshed from ZOHO_REFRESH_TOKEN in .env)
"""
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from src.config import settings
from src.context import current_token
from src.utils.errors import ManageEngineError, AuthError
from src.utils.logger import logger


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.TimeoutException):
        return True
    if isinstance(exc, ManageEngineError) and exc.status_code in (429, 502, 503, 504):
        return True
    return False


class MEClient:
    """ManageEngine Endpoint Central HTTP client."""

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=settings.me_base_url,
                timeout=httpx.Timeout(30.0),
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                follow_redirects=True,
            )
        return self._client

    async def _auth_header(self) -> dict[str, str]:
        # Prefer per-request token from Gemini; fall back to server-managed token
        token = current_token.get()
        if not token:
            from src.auth.token_manager import token_manager
            token = await token_manager.get_token()
        if not token:
            raise AuthError("No Zoho OAuth token available.")
        return {"Authorization": f"Zoho-oauthtoken {token}"}

    @retry(
        retry=retry_if_exception(_is_retryable),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        client = await self._get_client()
        headers = await self._auth_header()
        clean_params = {k: v for k, v in (params or {}).items() if v is not None} or None

        logger.debug(f"{method} {path} params={clean_params}")
        resp = await client.request(method, path, params=clean_params, json=json, headers=headers)

        if not resp.is_success:
            try:
                body = resp.json()
                msg = body.get("message_type") or body.get("message") or resp.text
                code = str(body.get("response_code", ""))
            except Exception:
                msg = resp.text
                code = ""
            raise ManageEngineError(msg, status_code=resp.status_code, response_code=code)

        try:
            return resp.json()
        except Exception:
            return resp.text

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, json: Any = None, params: dict[str, Any] | None = None) -> Any:
        return await self.request("POST", path, json=json, params=params)

    async def put(self, path: str, json: Any = None, params: dict[str, Any] | None = None) -> Any:
        return await self.request("PUT", path, json=json, params=params)

    async def delete(self, path: str, json: Any = None, params: dict[str, Any] | None = None) -> Any:
        return await self.request("DELETE", path, json=json, params=params)

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()


me_client = MEClient()
