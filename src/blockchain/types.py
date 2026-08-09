"""Type definitions for Blockchain.com API responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AddressInfo:
    """Information about a Bitcoin address."""

    address: str
    hash160: str = ""
    n_tx: int = 0
    total_received: int = 0
    total_sent: int = 0
    final_balance: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AddressInfo:
        return cls(
            address=data.get("address", ""),
            hash160=data.get("hash160", ""),
            n_tx=data.get("n_tx", 0),
            total_received=data.get("total_received", 0),
            total_sent=data.get("total_sent", 0),
            final_balance=data.get("final_balance", 0),
        )


@dataclass(frozen=True)
class Balance:
    """Balance summary for an address."""

    final_balance: int = 0
    n_tx: int = 0
    total_received: int = 0
    total_sent: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Balance:
        return cls(
            final_balance=data.get("final_balance", 0),
            n_tx=data.get("n_tx", 0),
            total_received=data.get("total_received", 0),
            total_sent=data.get("total_sent", 0),
        )


@dataclass(frozen=True)
class TransactionInput:
    """A single transaction input."""

    prev_out: dict[str, Any] = field(default_factory=dict)
    script: str = ""
    sequence: int = 0
    witness: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TransactionInput:
        return cls(
            prev_out=data.get("prev_out", {}),
            script=data.get("script", ""),
            sequence=data.get("sequence", 0),
            witness=data.get("witness", ""),
        )


@dataclass(frozen=True)
class TransactionOutput:
    """A single transaction output."""

    value: int = 0
    script: str = ""
    addr: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TransactionOutput:
        return cls(
            value=data.get("value", 0),
            script=data.get("script", ""),
            addr=data.get("addr", ""),
        )


@dataclass(frozen=True)
class Transaction:
    """A Bitcoin transaction."""

    hash: str = ""
    ver: int = 0
    vin_sz: int = 0
    vout_sz: int = 0
    size: int = 0
    weight: int = 0
    fee: int = 0
    time: int = 0
    block_height: int = 0
    block_hash: str = ""
    inputs: list[dict[str, Any]] = field(default_factory=list)
    out: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Transaction:
        return cls(
            hash=data.get("hash", ""),
            ver=data.get("ver", 0),
            vin_sz=data.get("vin_sz", 0),
            vout_sz=data.get("vout_sz", 0),
            size=data.get("size", 0),
            weight=data.get("weight", 0),
            fee=data.get("fee", 0),
            time=data.get("time", 0),
            block_height=data.get("block_height", 0),
            block_hash=data.get("block_hash", ""),
            inputs=data.get("inputs", []),
            out=data.get("out", []),
        )


@dataclass(frozen=True)
class Block:
    """A Bitcoin block."""

    hash: str = ""
    version: int = 0
    previous_block: str = ""
    merkle_root: str = ""
    time: int = 0
    bits: str = ""
    height: int = 0
    nonce: int = 0
    size: int = 0
    difficulty: float = 0.0
    tx: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Block:
        return cls(
            hash=data.get("hash", ""),
            version=data.get("ver", 0),
            previous_block=data.get("prev_block", ""),
            merkle_root=data.get("mrkl_root", ""),
            time=data.get("time", 0),
            bits=data.get("bits", ""),
            height=data.get("height", 0),
            nonce=data.get("nonce", 0),
            size=data.get("size", 0),
            difficulty=data.get("difficulty", 0.0),
            tx=data.get("tx", []),
        )


@dataclass(frozen=True)
class BlockHeight:
    """Block height query result."""

    blocks: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BlockHeight:
        return cls(blocks=data.get("blocks", []))


@dataclass(frozen=True)
class UnconfirmedTransaction:
    """An unconfirmed (pending) transaction."""

    hash: str = ""
    time: int = 0
    ver: int = 0
    vin_sz: int = 0
    vout_sz: int = 0
    size: int = 0
    weight: int = 0
    fee: int = 0
    inputs: list[dict[str, Any]] = field(default_factory=list)
    out: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UnconfirmedTransaction:
        return cls(
            hash=data.get("hash", ""),
            time=data.get("time", 0),
            ver=data.get("ver", 0),
            vin_sz=data.get("vin_sz", 0),
            vout_sz=data.get("vout_sz", 0),
            size=data.get("size", 0),
            weight=data.get("weight", 0),
            fee=data.get("fee", 0),
            inputs=data.get("inputs", []),
            out=data.get("out", []),
        )


@dataclass(frozen=True)
class UnspentOutput:
    """An unspent transaction output (UTXO)."""

    tx_hash: str = ""
    tx_hash_big_endian: str = ""
    tx_index: int = 0
    tx_output_n: int = 0
    script: str = ""
    value: int = 0
    value_hex: str = ""
    confirmations: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UnspentOutput:
        return cls(
            tx_hash=data.get("tx_hash", ""),
            tx_hash_big_endian=data.get("tx_hash_big_endian", ""),
            tx_index=data.get("tx_index", 0),
            tx_output_n=data.get("tx_output_n", 0),
            script=data.get("script", ""),
            value=data.get("value", 0),
            value_hex=data.get("value_hex", ""),
            confirmations=data.get("confirmations", 0),
        )


@dataclass(frozen=True)
class ChartValue:
    """A single data point in a chart."""

    x: int = 0
    y: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChartValue:
        return cls(x=data.get("x", 0), y=data.get("y", 0.0))


@dataclass(frozen=True)
class ChartData:
    """Response from the Charts API."""

    status: str = ""
    name: str = ""
    unit: str = ""
    period: str = ""
    description: str = ""
    values: list[ChartValue] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChartData:
        return cls(
            status=data.get("status", ""),
            name=data.get("name", ""),
            unit=data.get("unit", ""),
            period=data.get("period", ""),
            description=data.get("description", ""),
            values=[ChartValue.from_dict(v) for v in data.get("values", [])],
        )


@dataclass(frozen=True)
class TickerCurrency:
    """Ticker data for a single currency."""

    fifteen_min: float = 0.0
    last: float = 0.0
    buy: float = 0.0
    sell: float = 0.0
    symbol: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TickerCurrency:
        return cls(
            fifteen_min=data.get("15m", 0.0),
            last=data.get("last", 0.0),
            buy=data.get("buy", 0.0),
            sell=data.get("sell", 0.0),
            symbol=data.get("symbol", ""),
        )


@dataclass(frozen=True)
class Ticker:
    """Full ticker response with all currencies."""

    currencies: dict[str, TickerCurrency] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Ticker:
        return cls(
            currencies={k: TickerCurrency.from_dict(v) for k, v in data.items()}
        )


@dataclass(frozen=True)
class ExchangeRate:
    """A simplified exchange rate pair."""

    currency: str = ""
    fifteen_min: float = 0.0
    last: float = 0.0
    buy: float = 0.0
    sell: float = 0.0
    symbol: str = ""

    @classmethod
    def from_dict(cls, currency: str, data: dict[str, Any]) -> ExchangeRate:
        return cls(
            currency=currency,
            fifteen_min=data.get("15m", 0.0),
            last=data.get("last", 0.0),
            buy=data.get("buy", 0.0),
            sell=data.get("sell", 0.0),
            symbol=data.get("symbol", ""),
        )


@dataclass(frozen=True)
class MultiAddressInfo:
    """Information for a single address in a multi-address query."""

    address: str = ""
    hash160: str = ""
    n_tx: int = 0
    total_received: int = 0
    total_sent: int = 0
    final_balance: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MultiAddressInfo:
        return cls(
            address=data.get("address", ""),
            hash160=data.get("hash160", ""),
            n_tx=data.get("n_tx", 0),
            total_received=data.get("total_received", 0),
            total_sent=data.get("total_sent", 0),
            final_balance=data.get("final_balance", 0),
        )


@dataclass(frozen=True)
class MultiAddressResponse:
    """Response from the multi-address endpoint."""

    addresses: list[MultiAddressInfo] = field(default_factory=list)
    txs: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MultiAddressResponse:
        return cls(
            addresses=[
                MultiAddressInfo.from_dict(a) for a in data.get("addresses", [])
            ],
            txs=data.get("txs", []),
        )


@dataclass(frozen=True)
class LatestBlock:
    """The latest block information."""

    hash: str = ""
    time: int = 0
    block_index: int = 0
    height: int = 0
    txIndexes: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LatestBlock:
        return cls(
            hash=data.get("hash", ""),
            time=data.get("time", 0),
            block_index=data.get("block_index", 0),
            height=data.get("height", 0),
            txIndexes=data.get("txIndexes", 0),
        )


@dataclass(frozen=True)
class SimpleQueryResult:
    """Result from a Simple Query API call."""

    endpoint: str = ""
    value: Any = None

    @classmethod
    def from_raw(cls, endpoint: str, value: str) -> SimpleQueryResult:
        """Parse raw text response into appropriate type."""
        cleaned = value.strip()
        if cleaned.lstrip("-").isdigit():
            return cls(endpoint=endpoint, value=int(cleaned))
        try:
            return cls(endpoint=endpoint, value=float(cleaned))
        except ValueError:
            return cls(endpoint=endpoint, value=cleaned)
