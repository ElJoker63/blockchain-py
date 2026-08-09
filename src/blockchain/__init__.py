"""Async Python client for the Blockchain.com Explorer API."""

__version__ = "1.0.0"

from blockchain.blockchain import BlockchainAPI
from blockchain.charts import ChartsAPI
from blockchain.client import BlockchainClient
from blockchain.exchange_rates import ExchangeRatesAPI
from blockchain.simple_query import SimpleQueryAPI
from blockchain.types import (
    AddressInfo,
    Balance,
    Block,
    BlockHeight,
    ChartData,
    ChartValue,
    ExchangeRate,
    LatestBlock,
    MultiAddressInfo,
    MultiAddressResponse,
    SimpleQueryResult,
    Ticker,
    TickerCurrency,
    Transaction,
    TransactionInput,
    TransactionOutput,
    UnconfirmedTransaction,
    UnspentOutput,
)
from blockchain.websocket import BlockchainWebSocket

__all__ = [
    # Client
    "BlockchainClient",
    # Sub-APIs
    "BlockchainAPI",
    "ChartsAPI",
    "ExchangeRatesAPI",
    "SimpleQueryAPI",
    "BlockchainWebSocket",
    # Types
    "AddressInfo",
    "Balance",
    "Block",
    "BlockHeight",
    "ChartData",
    "ChartValue",
    "ExchangeRate",
    "LatestBlock",
    "MultiAddressInfo",
    "MultiAddressResponse",
    "SimpleQueryResult",
    "Ticker",
    "TickerCurrency",
    "Transaction",
    "TransactionInput",
    "TransactionOutput",
    "UnconfirmedTransaction",
    "UnspentOutput",
]
