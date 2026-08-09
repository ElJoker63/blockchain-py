# blockchain-api

Async Python client for the [Blockchain.com Explorer API](https://www.blockchain.com/explorer/docs).

> **Author:** ElJoker63 · **Email:** eljoker63@udyat.site

## Installation

```bash
pip install blockchain-api
```

## Quick Start

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        # Latest block
        block = await client.blockchain.get_latest_block()
        print(f"Block #{block.height}: {block.hash[:16]}...")

        # Ticker / price
        ticker = await client.exchange.get_ticker()
        print(f"BTC/USD: ${ticker.currencies['USD'].last:,.2f}")

        # Address balance
        addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        balance = await client.blockchain.get_balance([addr])
        print(f"Balance: {balance[addr]['final_balance'] / 1e8} BTC")

asyncio.run(main())
```

---

## API Reference

### `BlockchainClient`

The unified entry point. Use as an async context manager for automatic cleanup.

```python
async with BlockchainClient() as client:
    ...
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `timeout` | `float` | `30.0` | HTTP request timeout (seconds) |
| `headers` | `dict` | `None` | Extra HTTP headers |
| `max_connections` | `int` | `20` | Connection pool size |
| `max_keepalive` | `int` | `10` | Keep-alive pool size |

**Attributes:**

| Attribute | Type | Description |
|---|---|---|
| `client.blockchain` | `BlockchainAPI` | Blocks, transactions, addresses, UTXOs |
| `client.simple` | `SimpleQueryAPI` | Plain-text one-liner endpoints |
| `client.exchange` | `ExchangeRatesAPI` | Ticker data and currency conversion |
| `client.charts` | `ChartsAPI` | Historical chart data |
| `client.websocket()` | → `BlockchainWebSocket` | Real-time WebSocket events |

---

### Blockchain Data API (`client.blockchain`)

#### Blocks

```python
# By hash
block = await client.blockchain.get_block("000000000000000000024bead8df69990852c202db0e00ec78d2700b6dae337c")

# By height
block_height = await client.blockchain.get_block_by_height(700000)

# Latest block
latest = await client.blockchain.get_latest_block()

# By timestamp (ms)
blocks = await client.blockchain.get_blocks_by_time(1234567890000)

# By mining pool
blocks = await client.blockchain.get_blocks_by_pool("antpool")
```

#### Transactions

```python
tx = await client.blockchain.get_transaction("b6f699...")

# Raw hex format
tx_hex = await client.blockchain.get_transaction("b6f699...", as_hex=True)

# All pending transactions
pending = await client.blockchain.get_unconfirmed_transactions()
```

#### Addresses

```python
# Single address
info = await client.blockchain.get_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

# Multiple addresses (also supports xpubs)
multi = await client.blockchain.get_multi_address(["addr1", "addr2"])
```

#### Balance

```python
balances = await client.blockchain.get_balance(["addr1", "addr2"])
# Returns: {"addr1": {"final_balance": 50000, "n_tx": 10, ...}, ...}
```

#### Unspent Outputs (UTXOs)

```python
utxos = await client.blockchain.get_unspent_outputs(
    ["addr1"],
    limit=100,
    confirmations=6,
)
```

---

### Simple Query API (`client.simple`)

> ⚠️ Rate limit: **1 request every 10 seconds.**

All values are returned as `SimpleQueryResult` objects (auto-parsed to `int`, `float`, or `str`).

#### Network Stats

```python
difficulty = await client.simple.get_difficulty()
block_count = await client.simple.get_block_count()
latest_hash = await client.simple.get_latest_hash()
bc_per_block = await client.simple.get_bc_per_block()
total_bc = await client.simple.get_total_bc()
probability = await client.simple.get_probability()
hashes_to_win = await client.simple.get_hashes_to_win()
next_retarget = await client.simple.get_next_retarget()
avg_tx_size = await client.simple.get_avg_tx_size(2000)
avg_tx_value = await client.simple.get_avg_tx_value()
interval = await client.simple.get_interval()
eta = await client.simple.get_eta()
avg_tx_number = await client.simple.get_avg_tx_number(100)
hashrate = await client.simple.get_hashrate()
```

#### Address Queries

```python
received = await client.simple.get_received_by_address("1A1z...")
sent = await client.simple.get_sent_by_address("1A1z...")
balance = await client.simple.get_address_balance("1A1z...")
first_seen = await client.simple.get_address_first_seen("1A1z...")
```

#### Conversion Tools

```python
h160 = await client.simple.address_to_hash("1A1z...")
addr = await client.simple.hash_to_address("62e907b15cbf...")
h160_from_key = await client.simple.hash_pubkey("04...")
addr_from_key = await client.simple.addr_pubkey("04...")
pubkey = await client.simple.pubkey_addr("1A1z...")
```

#### Transaction Lookups

```python
total_out = await client.simple.tx_total_btc_output("b6f699...")
total_in = await client.simple.tx_total_btc_input("b6f699...")
fee = await client.simple.tx_fee("b6f699...")
result = await client.simple.tx_result("b6f699...", "1A1z...")
```

#### Market Data

```python
price = await client.simple.get_24hr_price()
market_cap = await client.simple.get_market_cap()
tx_count = await client.simple.get_24hr_tx_count()
btc_sent = await client.simple.get_24hr_btc_sent()
```

#### Misc

```python
unconfirmed = await client.simple.get_unconfirmed_count()
rejected = await client.simple.get_rejected("tx_or_block_hash")
```

---

### Exchange Rates API (`client.exchange`)

```python
# Full ticker
ticker = await client.exchange.get_ticker()
for code, data in ticker.currencies.items():
    print(f"{code}: {data.symbol}{data.last:,.2f}")

# Single currency
usd = await client.exchange.get_exchange_rate("USD")
print(f"Buy: {usd.symbol}{usd.buy:,.2f}  Sell: {usd.symbol}{usd.sell:,.2f}")

# Convert fiat → BTC
btc_amount = await client.exchange.to_btc("USD", 1000)
print(f"$1,000 = {btc_amount} BTC")
```

---

### Charts & Statistics API (`client.charts`)

```python
# Fetch JSON chart data
chart = await client.charts.get_chart(
    "bitcoin-price",
    timespan="5years",
    rolling_average="8hours",
    sampled=True,
)
for point in chart.values[:5]:
    print(f"  {point.x}: ${point.y:,.2f}")

# Fetch raw CSV
csv_data = await client.charts.get_chart_raw(
    "n-transactions",
    timespan="3months",
)

# List all available charts
print(client.charts.list_available_charts())
```

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chart_name` | `str` | *required* | Chart identifier (e.g. `"bitcoin-price"`) |
| `timespan` | `str` | `None` | Duration: `"5weeks"`, `"1year"`, `"3months"`, etc. |
| `rolling_average` | `str` | `None` | Averaging window: `"8hours"`, etc. |
| `start` | `str` | `None` | Start date: `"YYYY-MM-DD"` or `"YYYY-MM-DDThh:mm:ss"` |
| `format` | `str` | `"json"` | `"json"` or `"csv"` |
| `sampled` | `bool` | `True` | Limit to ~1500 datapoints |

---

### WebSocket Streaming (`client.websocket()`)

```python
import asyncio
from blockchain import BlockchainClient

async def on_block(block: dict):
    print(f"New block #{block['height']}: {block['hash'][:16]}...")

async def on_tx(tx: dict):
    total = sum(o["value"] for o in tx.get("out", []))
    print(f"New tx {tx['hash'][:16]}...  value={total/1e8:.8f} BTC")

async def main():
    async with BlockchainClient() as client:
        ws = client.websocket()

        ws.on_block(on_block)
        ws.on_transaction(on_tx)

        await ws.connect()
        await ws.subscribe_new_blocks()
        await ws.subscribe_unconfirmed_transactions()

        # Run in background while doing other work
        task = await ws.start_background()
        await asyncio.sleep(60)  # Listen for 60 seconds
        await ws.close()

asyncio.run(main())
```

#### WebSocket Methods

| Method | Description |
|---|---|
| `connect()` | Open the WebSocket connection |
| `close()` | Close connection and stop receive loop |
| `subscribe_new_blocks()` | Subscribe to new block notifications |
| `unsubscribe_new_blocks()` | Unsubscribe from blocks |
| `subscribe_unconfirmed_transactions()` | Subscribe to mempool transactions |
| `unsubscribe_unconfirmed_transactions()` | Unsubscribe from mempool |
| `subscribe_address(address)` | Subscribe to txs for a specific address |
| `unsubscribe_address(address)` | Unsubscribe from an address |
| `ping()` | Send a keep-alive ping |
| `ping_block()` | Request latest block immediately |
| `ping_transaction()` | Request latest tx immediately |
| `run_forever()` | Block until connection closes |
| `start_background()` | Start receive loop as a background task |

#### Handler Registration

```python
ws.on_block(handler)        # Called with the "x" payload of block messages
ws.on_transaction(handler)  # Called with the "x" payload of utx messages
ws.on_message(handler)      # Called with the entire raw message
```

---

## Types Reference

All types are frozen `dataclass` instances:

| Type | Description |
|---|---|
| `Block` | Block with hash, height, merkle root, transactions |
| `BlockHeight` | Block height query result (list of blocks) |
| `LatestBlock` | Latest block summary |
| `Transaction` | Full transaction with inputs/outputs |
| `TransactionInput` | Single transaction input |
| `TransactionOutput` | Single transaction output |
| `AddressInfo` | Address summary (balance, tx count, etc.) |
| `Balance` | Balance result for an address |
| `MultiAddressInfo` | Address info in multi-address response |
| `MultiAddressResponse` | Multi-address query result |
| `UnspentOutput` | UTXO with value, script, confirmations |
| `UnconfirmedTransaction` | Pending transaction |
| `ChartData` | Chart response with values array |
| `ChartValue` | Single datapoint `{x: timestamp, y: value}` |
| `Ticker` | Full ticker with all currencies |
| `TickerCurrency` | Ticker for one currency |
| `ExchangeRate` | Simplified exchange rate |
| `SimpleQueryResult` | Plain-text result (auto-parsed) |

## License

MIT
