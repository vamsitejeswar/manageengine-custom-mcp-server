"""Zoho OAuth token manager — auto-refreshes access token using a stored refresh token."""
import asyncio
import time
from typing import Optional

import httpx

from src.config import settings
from src.utils.logger import logger


class ZohoTokenManager:
    def __init__(self) -> None:
        self._access_token: str = ""
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    def _is_expired(self) -> bool:
        # Refresh 60s before actual expiry
        return time.monotonic() >= (self._expires_at - 60)

    async def get_token(self) -> str:
        if not self._is_expired() and self._access_token:
            return self._access_token

        async with self._lock:
            # Double-check after acquiring lock
            if not self._is_expired() and self._access_token:
                return self._access_token
            await self._refresh()
            return self._access_token

    async def _refresh(self) -> None:
        if not all([settings.zoho_client_id, settings.zoho_client_secret, settings.zoho_refresh_token]):
            raise RuntimeError(
                "Zoho OAuth credentials not configured. "
                "Set ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN in .env"
            )

        logger.info("Refreshing Zoho access token...")
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                settings.zoho_token_url,
                data={
                    "grant_type": "refresh_token",
                    "client_id": settings.zoho_client_id,
                    "client_secret": settings.zoho_client_secret,
                    "refresh_token": settings.zoho_refresh_token,
                },
            )
            resp.raise_for_status()
            body = resp.json()

        if "access_token" not in body:
            raise RuntimeError(f"Token refresh failed: {body}")

        self._access_token = body["access_token"]
        expires_in = int(body.get("expires_in", 3600))
        self._expires_at = time.monotonic() + expires_in
        logger.info(f"Zoho token refreshed, valid for {expires_in}s")


token_manager = ZohoTokenManager()
