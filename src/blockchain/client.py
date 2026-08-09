"""Unified async client for the Blockchain.com Explorer API."""

from __future__ import annotations

from blockchain._http import HTTPClient
from blockchain.blockchain import BlockchainAPI
from blockchain.charts import ChartsAPI
from blockchain.exchange_rates import ExchangeRatesAPI
from blockchain.simple_query import SimpleQueryAPI
from blockchain.websocket import BlockchainWebSocket


class BlockchainClient:
    """One-stop async client for the entire Blockchain.com Explorer API.

    Access sub-APIs via the named attributes and use the context-manager
    for automatic resource cleanup::

        async with BlockchainClient() as client:
            ticker = await client.exchange.get_ticker()
            block  = await client.blockchain.get_latest_block()
            print(block.height, ticker.currencies["USD"].last)

    Parameters
    ----------
    timeout:
        HTTP request timeout in seconds (default 30).
    headers:
        Extra headers sent with every HTTP request.
    max_connections:
        Connection pool size for ``httpx``.
    max_keepalive:
        Keep-alive pool size for ``httpx``.
    """

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        max_connections: int = 20,
        max_keepalive: int = 10,
    ) -> None:
        self._http = HTTPClient(
            timeout=timeout,
            headers=headers,
            max_connections=max_connections,
            max_keepalive=max_keepalive,
        )
        self.blockchain = BlockchainAPI(self._http)
        """Blockchain Data API — blocks, transactions, addresses, UTXOs."""

        self.simple = SimpleQueryAPI(self._http)
        """Simple Query API — plain-text one-liner endpoints."""

        self.exchange = ExchangeRatesAPI(self._http)
        """Exchange Rates API — ticker and currency conversion."""

        self.charts = ChartsAPI(self._http)
        """Charts & Statistics API — historical data feeds."""

    def websocket(self, url: str | None = None) -> BlockchainWebSocket:
        """Create a new WebSocket client for real-time events.

        Parameters
        ----------
        url:
            Override the default WebSocket URL
            (``wss://ws.blockchain.info/inv``).

        Returns
        -------
        BlockchainWebSocket
            An unconnected WebSocket client. Use it as an async context
            manager or call ``connect()`` manually.
        """
        ws = BlockchainWebSocket(url=url or "wss://ws.blockchain.info/inv")
        return ws

    async def close(self) -> None:
        """Close all underlying HTTP connections."""
        await self._http.close()

    async def __aenter__(self) -> BlockchainClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
