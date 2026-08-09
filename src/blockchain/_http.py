"""HTTP transport layer for Blockchain.com API."""

from __future__ import annotations

from typing import Any

import httpx


class HTTPClient:
    """Internal async HTTP client wrapper."""

    BASE_URL = "https://blockchain.info"
    CHARTS_BASE_URL = "https://api.blockchain.info"
    RATE_LIMIT_DELAY = 10.0  # seconds between simple query calls

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        max_connections: int = 20,
        max_keepalive: int = 10,
    ) -> None:
        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive,
        )
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=httpx.Timeout(timeout),
            limits=limits,
            headers=headers or {},
        )

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    async def get_json(
        self, path: str, params: dict[str, str | int | float | None] | None = None
    ) -> dict[str, Any]:
        """GET request returning parsed JSON dict."""
        response = await self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    async def get_json_from(
        self,
        base_url: str,
        path: str,
        params: dict[str, str | int | float | None] | None = None,
    ) -> dict[str, Any]:
        """GET request to a different base URL, returning parsed JSON."""
        response = await self._client.get(
            f"{base_url}{path}", params=params
        )
        response.raise_for_status()
        return response.json()

    async def get_text(
        self, path: str, params: dict[str, str | int | float | None] | None = None
    ) -> str:
        """GET request returning raw text."""
        response = await self._client.get(path, params=params)
        response.raise_for_status()
        return response.text

    async def get_text_from(
        self,
        base_url: str,
        path: str,
        params: dict[str, str | int | float | None] | None = None,
    ) -> str:
        """GET request to a different base URL, returning raw text."""
        response = await self._client.get(
            f"{base_url}{path}", params=params
        )
        response.raise_for_status()
        return response.text

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> HTTPClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
