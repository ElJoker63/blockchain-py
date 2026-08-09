"""Blockchain Data API — raw blocks, transactions, addresses, UTXOs."""

from __future__ import annotations

from typing import Any

from blockchain._http import HTTPClient
from blockchain.types import (
    AddressInfo,
    Block,
    BlockHeight,
    LatestBlock,
    MultiAddressResponse,
    Transaction,
    UnconfirmedTransaction,
    UnspentOutput,
)


class BlockchainAPI:
    """Async wrapper for the Blockchain.com Data API.

    All methods return typed dataclasses from :mod:`blockchain.types`.
    """

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    # ── Blocks ────────────────────────────────────────────────────────

    async def get_block(self, block_hash: str, *, as_hex: bool = False) -> Block:
        """Fetch a single block by its hash.

        Parameters
        ----------
        block_hash:
            The SHA-256 hash of the block.
        as_hex:
            If *True*, the raw binary form is returned (hex-encoded).
        """
        params: dict[str, str] = {}
        if as_hex:
            params["format"] = "hex"
        data = await self._http.get_json(f"/rawblock/{block_hash}", params=params)
        return Block.from_dict(data)

    async def get_block_by_height(self, height: int) -> BlockHeight:
        """Fetch block(s) at a given height.

        Parameters
        ----------
        height:
            The block height (chain index).
        """
        data = await self._http.get_json(
            f"/block-height/{height}", params={"format": "json"}
        )
        return BlockHeight.from_dict(data)

    async def get_latest_block(self) -> LatestBlock:
        """Fetch the latest block in the longest chain."""
        data = await self._http.get_json("/latestblock")
        return LatestBlock.from_dict(data)

    async def get_blocks_by_time(self, time_ms: int) -> dict[str, Any]:
        """Fetch blocks mined at a given timestamp (milliseconds).

        Parameters
        ----------
        time_ms:
            Unix timestamp in milliseconds.
        """
        return await self._http.get_json(
            f"/blocks/{time_ms}", params={"format": "json"}
        )

    async def get_blocks_by_pool(self, pool_name: str) -> dict[str, Any]:
        """Fetch blocks mined by a specific pool.

        Parameters
        ----------
        pool_name:
            The name of the mining pool.
        """
        return await self._http.get_json(
            f"/blocks/{pool_name}", params={"format": "json"}
        )

    # ── Transactions ──────────────────────────────────────────────────

    async def get_transaction(self, tx_hash: str, *, as_hex: bool = False) -> Transaction:
        """Fetch a single transaction by its hash.

        Parameters
        ----------
        tx_hash:
            The transaction hash.
        as_hex:
            If *True*, return the raw binary hex representation.
        """
        params: dict[str, str] = {}
        if as_hex:
            params["format"] = "hex"
        data = await self._http.get_json(f"/rawtx/{tx_hash}", params=params)
        return Transaction.from_dict(data)

    async def get_unconfirmed_transactions(self) -> list[UnconfirmedTransaction]:
        """Fetch all currently unconfirmed (pending) transactions."""
        data = await self._http.get_json(
            "/unconfirmed-transactions", params={"format": "json"}
        )
        return [UnconfirmedTransaction.from_dict(tx) for tx in data.get("txs", [])]

    # ── Addresses ─────────────────────────────────────────────────────

    async def get_address(
        self,
        address: str,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Fetch detailed information for a single Bitcoin address.

        Parameters
        ----------
        address:
            Base58 or hash160 Bitcoin address.
        limit:
            Number of transactions to return (max 50).
        offset:
            Number of transactions to skip for pagination.
        """
        params: dict[str, str | int] = {"limit": limit, "offset": offset}
        return await self._http.get_json(f"/rawaddr/{address}", params=params)

    async def get_multi_address(
        self,
        addresses: list[str],
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> MultiAddressResponse:
        """Fetch information for multiple addresses (or xpubs) at once.

        Parameters
        ----------
        addresses:
            List of base58 or xpub addresses.
        limit:
            Number of transactions to show (max 100).
        offset:
            Skip the first *n* transactions.
        """
        active = "|".join(addresses)
        params: dict[str, str | int] = {"active": active, "n": limit, "offset": offset}
        data = await self._http.get_json("/multiaddr", params=params)
        return MultiAddressResponse.from_dict(data)

    # ── Balance ───────────────────────────────────────────────────────

    async def get_balance(self, addresses: list[str]) -> dict[str, dict[str, int]]:
        """Fetch balance for one or more addresses.

        Parameters
        ----------
        addresses:
            List of base58 or xpub addresses, pipe-separated internally.

        Returns
        -------
        dict
            Mapping of address → ``{final_balance, n_tx, total_received}``.
        """
        active = "|".join(addresses)
        return await self._http.get_json("/balance", params={"active": active})

    # ── UTXOs ─────────────────────────────────────────────────────────

    async def get_unspent_outputs(
        self,
        addresses: list[str],
        *,
        limit: int = 250,
        confirmations: int | None = None,
    ) -> list[UnspentOutput]:
        """Fetch unspent transaction outputs (UTXOs).

        Parameters
        ----------
        addresses:
            List of base58 or xpub addresses.
        limit:
            Number of UTXOs to return (max 1000).
        confirmations:
            Minimum number of confirmations required.
        """
        active = "|".join(addresses)
        params: dict[str, str | int] = {"active": active, "limit": limit}
        if confirmations is not None:
            params["confirmations"] = confirmations
        data = await self._http.get_json("/unspent", params=params)
        return [
            UnspentOutput.from_dict(u) for u in data.get("unspent_outputs", [])
        ]
