"""WebSocket streaming — real-time blocks and transactions."""

from __future__ import annotations

import asyncio
import json
from typing import Any, Callable, Awaitable

import websockets
import websockets.exceptions


WS_URL = "wss://ws.blockchain.info/inv"


class BlockchainWebSocket:
    """Async WebSocket client for real-time blockchain events.

    Connects to ``wss://ws.blockchain.info/inv`` and provides typed
    subscription helpers for blocks, transactions, and address events.

    Usage::

        async with BlockchainWebSocket() as ws:
            ws.on_block(my_handler)
            ws.on_transaction(my_handler)
            await ws.connect()
            await ws.subscribe_new_blocks()
            await ws.subscribe_unconfirmed_transactions()
            await ws.subscribe_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
            await ws.run_forever()
    """

    def __init__(self, url: str = WS_URL) -> None:
        self._url = url
        self._ws: Any = None
        self._block_handlers: list[Callable[[dict[str, Any]], Awaitable[None]]] = []
        self._tx_handlers: list[Callable[[dict[str, Any]], Awaitable[None]]] = []
        self._message_handlers: list[Callable[[dict[str, Any]], Awaitable[None]]] = []
        self._running = False
        self._receive_task: asyncio.Task[None] | None = None

    # ── Connection management ─────────────────────────────────────────

    async def connect(self) -> None:
        """Open the WebSocket connection."""
        self._ws = await websockets.connect(self._url)

    async def close(self) -> None:
        """Close the WebSocket connection and stop the receive loop."""
        self._running = False
        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def __aenter__(self) -> BlockchainWebSocket:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    # ── Handler registration ──────────────────────────────────────────

    def on_block(
        self, handler: Callable[[dict[str, Any]], Awaitable[None]]
    ) -> None:
        """Register a handler for new block events.

        The handler receives the full ``x`` payload from the WebSocket message.
        """
        self._block_handlers.append(handler)

    def on_transaction(
        self, handler: Callable[[dict[str, Any]], Awaitable[None]]
    ) -> None:
        """Register a handler for new transaction events (address subscriptions).

        The handler receives the full ``x`` payload from the WebSocket message.
        """
        self._tx_handlers.append(handler)

    def on_message(
        self, handler: Callable[[dict[str, Any]], Awaitable[None]]
    ) -> None:
        """Register a handler for ALL incoming messages (raw)."""
        self._message_handlers.append(handler)

    # ── Subscription operations ───────────────────────────────────────

    async def _send(self, op: str, **extra: str) -> None:
        """Send an OP message."""
        if not self._ws:
            raise RuntimeError("WebSocket is not connected. Call connect() first.")
        msg = {"op": op}
        msg.update(extra)
        await self._ws.send(json.dumps(msg))

    async def subscribe_new_blocks(self) -> None:
        """Subscribe to new block notifications."""
        await self._send("blocks_sub")

    async def unsubscribe_new_blocks(self) -> None:
        """Unsubscribe from new block notifications."""
        await self._send("blocks_unsub")

    async def subscribe_unconfirmed_transactions(self) -> None:
        """Subscribe to all unconfirmed (mempool) transactions."""
        await self._send("unconfirmed_sub")

    async def unsubscribe_unconfirmed_transactions(self) -> None:
        """Unsubscribe from unconfirmed transactions."""
        await self._send("unconfirmed_unsub")

    async def subscribe_address(self, address: str) -> None:
        """Subscribe to transactions affecting a specific Bitcoin address.

        Parameters
        ----------
        address:
            A base58 Bitcoin address.
        """
        await self._send("addr_sub", addr=address)

    async def unsubscribe_address(self, address: str) -> None:
        """Unsubscribe from a specific address."""
        await self._send("addr_unsub", addr=address)

    async def ping(self) -> None:
        """Send a ping to keep the connection alive."""
        await self._send("ping")

    async def ping_block(self) -> None:
        """Request the latest block be sent immediately."""
        await self._send("ping_block")

    async def ping_transaction(self) -> None:
        """Request the latest transaction be sent immediately."""
        await self._send("ping_tx")

    # ── Receive loop ──────────────────────────────────────────────────

    async def _dispatch(self, data: dict[str, Any]) -> None:
        """Dispatch a received message to registered handlers."""
        op = data.get("op", "")

        for handler in self._message_handlers:
            try:
                await handler(data)
            except Exception:
                pass  # Don't let a bad handler break the loop

        if op == "block":
            for handler in self._block_handlers:
                try:
                    await handler(data.get("x", {}))
                except Exception:
                    pass

        if op == "utx":
            for handler in self._tx_handlers:
                try:
                    await handler(data.get("x", {}))
                except Exception:
                    pass

    async def _receive_loop(self) -> None:
        """Internal loop that reads messages and dispatches them."""
        self._running = True
        while self._running:
            try:
                if not self._ws:
                    break
                raw = await self._ws.recv()
                data = json.loads(raw)
                await self._dispatch(data)
            except websockets.exceptions.ConnectionClosed:
                break
            except asyncio.CancelledError:
                break
            except Exception:
                continue

    async def run_forever(self) -> None:
        """Start the receive loop. Blocks until the connection closes."""
        if not self._ws:
            raise RuntimeError("WebSocket is not connected. Call connect() first.")
        await self._receive_loop()

    async def start_background(self) -> asyncio.Task[None]:
        """Start the receive loop as a background task.

        Returns the task so you can await or cancel it.
        """
        if not self._ws:
            raise RuntimeError("WebSocket is not connected. Call connect() first.")
        self._receive_task = asyncio.create_task(self._receive_loop())
        return self._receive_task
