"""Simple Query API — plain-text one-liner endpoints.

Rate limit: 1 request every 10 seconds.
All BTC values are in Satoshi (divide by 100_000_000 for BTC).
"""

from __future__ import annotations

from blockchain._http import HTTPClient
from blockchain.types import SimpleQueryResult


class SimpleQueryAPI:
    """Async wrapper for the Blockchain.com Simple Query API.

    These endpoints return plain-text values, not JSON.
    """

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    async def _get(self, endpoint: str) -> SimpleQueryResult:
        raw = await self._http.get_text(f"/q/{endpoint}")
        return SimpleQueryResult.from_raw(endpoint, raw)

    # ── Network stats ─────────────────────────────────────────────────

    async def get_difficulty(self) -> SimpleQueryResult:
        """Current difficulty target as a decimal."""
        return await self._get("getdifficulty")

    async def get_block_count(self) -> SimpleQueryResult:
        """Current block height in the longest chain."""
        return await self._get("getblockcount")

    async def get_latest_hash(self) -> SimpleQueryResult:
        """Hash of the latest block."""
        return await self._get("latesthash")

    async def get_bc_per_block(self) -> SimpleQueryResult:
        """Current block reward in BTC."""
        return await self._get("bcperblock")

    async def get_total_bc(self) -> SimpleQueryResult:
        """Total BTC in circulation (delayed up to 1 hour). In Satoshi."""
        return await self._get("totalbc")

    async def get_probability(self) -> SimpleQueryResult:
        """Probability of finding a valid block per hash."""
        return await self._get("probability")

    async def get_hashes_to_win(self) -> SimpleQueryResult:
        """Average hash attempts needed to solve a block."""
        return await self._get("hashestowin")

    async def get_next_retarget(self) -> SimpleQueryResult:
        """Block height of the next difficulty re-target."""
        return await self._get("nextretarget")

    async def get_avg_tx_size(self, blocks: int | None = None) -> SimpleQueryResult:
        """Average transaction size for past *N* blocks (default 1000)."""
        path = f"avgtxsize/{blocks}" if blocks else "avgtxsize"
        return await self._get(path)

    async def get_avg_tx_value(self, blocks: int | None = None) -> SimpleQueryResult:
        """Average transaction value for past *N* blocks (default 1000)."""
        path = f"avgtxvalue/{blocks}" if blocks else "avgtxvalue"
        return await self._get(path)

    async def get_interval(self) -> SimpleQueryResult:
        """Average time between blocks in seconds."""
        return await self._get("interval")

    async def get_eta(self) -> SimpleQueryResult:
        """Estimated time until next block (seconds)."""
        return await self._get("eta")

    async def get_avg_tx_number(self, blocks: int | None = None) -> SimpleQueryResult:
        """Average transactions per block for past *N* blocks (default 100)."""
        path = f"avgtxnumber/{blocks}" if blocks else "avgtxnumber"
        return await self._get(path)

    async def get_hashrate(self) -> SimpleQueryResult:
        """Estimated network hash rate in gigahash."""
        return await self._get("hashrate")

    # ── Address queries ───────────────────────────────────────────────

    async def get_received_by_address(self, address: str) -> SimpleQueryResult:
        """Total BTC received by an address (in Satoshi)."""
        return await self._get(f"getreceivedbyaddress/{address}")

    async def get_sent_by_address(self, address: str) -> SimpleQueryResult:
        """Total BTC sent by an address (in Satoshi)."""
        return await self._get(f"getsentbyaddress/{address}")

    async def get_address_balance(self, address: str) -> SimpleQueryResult:
        """Balance of a single address (in Satoshi)."""
        return await self._get(f"addressbalance/{address}")

    async def get_address_first_seen(self, address: str) -> SimpleQueryResult:
        """Timestamp of the block when the address was first confirmed."""
        return await self._get(f"addressfirstseen/{address}")

    # ── Conversion tools ──────────────────────────────────────────────

    async def address_to_hash(self, address: str) -> SimpleQueryResult:
        """Convert a Bitcoin address to its hash160."""
        return await self._get(f"addresstohash/{address}")

    async def hash_to_address(self, hash160: str) -> SimpleQueryResult:
        """Convert a hash160 to a Bitcoin address."""
        return await self._get(f"hashtoaddress/{hash160}")

    async def hash_pubkey(self, pubkey: str) -> SimpleQueryResult:
        """Convert a public key to hash160."""
        return await self._get(f"hashpubkey/{pubkey}")

    async def addr_pubkey(self, pubkey: str) -> SimpleQueryResult:
        """Convert a public key to a Bitcoin address."""
        return await self._get(f"addrpubkey/{pubkey}")

    async def pubkey_addr(self, address: str) -> SimpleQueryResult:
        """Convert an address to its public key (if available)."""
        return await self._get(f"pubkeyaddr/{address}")

    # ── Transaction queries ───────────────────────────────────────────

    async def tx_total_btc_output(self, tx_hash: str) -> SimpleQueryResult:
        """Total output value of a transaction (in Satoshi)."""
        return await self._get(f"txtotalbtcoutput/{tx_hash}")

    async def tx_total_btc_input(self, tx_hash: str) -> SimpleQueryResult:
        """Total input value of a transaction (in Satoshi)."""
        return await self._get(f"txtotalbtcinput/{tx_hash}")

    async def tx_fee(self, tx_hash: str) -> SimpleQueryResult:
        """Fee included in a transaction (in Satoshi)."""
        return await self._get(f"txfee/{tx_hash}")

    async def tx_result(self, tx_hash: str, address: str) -> SimpleQueryResult:
        """Result of a transaction sent/received to an address."""
        return await self._get(f"txresult/{tx_hash}/{address}")

    # ── Market data ───────────────────────────────────────────────────

    async def get_24hr_price(self) -> SimpleQueryResult:
        """24-hour weighted price from largest exchanges (USD)."""
        return await self._get("24hrprice")

    async def get_market_cap(self) -> SimpleQueryResult:
        """USD market cap (based on 24-hour weighted price)."""
        return await self._get("marketcap")

    async def get_24hr_tx_count(self) -> SimpleQueryResult:
        """Number of transactions in the past 24 hours."""
        return await self._get("24hrtransactioncount")

    async def get_24hr_btc_sent(self) -> SimpleQueryResult:
        """BTC sent in the last 24 hours (in Satoshi)."""
        return await self._get("24hrbtcsent")

    # ── Misc ──────────────────────────────────────────────────────────

    async def get_unconfirmed_count(self) -> SimpleQueryResult:
        """Number of pending unconfirmed transactions."""
        return await self._get("unconfirmedcount")

    async def get_rejected(self, query: str) -> SimpleQueryResult:
        """Reason why a tx or block hash was rejected (if any)."""
        return await self._get(f"rejected/{query}")
