# Blockchain Data API

Acceso a bloques, transacciones, direcciones y UTXOs de Bitcoin.

```python
api = client.blockchain
```

## Bloques

### `get_block(block_hash, *, as_hex=False)`

Obtiene un bloque por su hash.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `block_hash` | `str` | Hash SHA-256 del bloque |
| `as_hex` | `bool` | Si `True`, devuelve el formato binario hex |

**Retorna:** `Block`

```python
block = await client.blockchain.get_block(
    "000000000000000000024bead8df69990852c202db0e00ec78d2700b6dae337c"
)
print(f"Altura: {block.height}, Nonce: {block.nonce}")
```

### `get_block_by_height(height)`

Obtiene uno o más bloques en una altura específica.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `height` | `int` | Altura del bloque en la cadena |

**Retorna:** `BlockHeight`

```python
result = await client.blockchain.get_block_by_height(700000)
for b in result.blocks:
    print(b["hash"])
```

### `get_latest_block()`

Obtiene el último bloque de la cadena más larga.

**Retorna:** `LatestBlock`

```python
latest = await client.blockchain.get_latest_block()
print(f"Bloque #{latest.height}: {latest.hash}")
```

### `get_blocks_by_time(time_ms)`

Obtiene bloques minados en un timestamp específico.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `time_ms` | `int` | Timestamp Unix en milisegundos |

**Retorna:** `dict`

```python
blocks = await client.blockchain.get_blocks_by_time(1234567890000)
```

### `get_blocks_by_pool(pool_name)`

Obtiene bloques minados por un pool específico.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `pool_name` | `str` | Nombre del pool minero |

**Retorna:** `dict`

```python
blocks = await client.blockchain.get_blocks_by_pool("antpool")
```

## Transacciones

### `get_transaction(tx_hash, *, as_hex=False)`

Obtiene una transacción por su hash.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tx_hash` | `str` | Hash de la transacción |
| `as_hex` | `bool` | Si `True`, devuelve formato binario hex |

**Retorna:** `Transaction`

```python
tx = await client.blockchain.get_transaction("b6f699...")
print(f"Inputs: {tx.vin_sz}, Outputs: {tx.vout_sz}")
```

### `get_unconfirmed_transactions()`

Obtiene todas las transacciones pendientes (mempool).

**Retorna:** `list[UnconfirmedTransaction]`

```python
pending = await client.blockchain.get_unconfirmed_transactions()
print(f"Transacciones pendientes: {len(pending)}")
```

## Direcciones

### `get_address(address, *, limit=50, offset=0)`

Obtiene información detallada de una dirección Bitcoin.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `address` | `str` | Dirección base58 o hash160 |
| `limit` | `int` | Nº de transacciones (máx 50) |
| `offset` | `int` | Saltar las primeras N transacciones |

**Retorna:** `dict`

```python
info = await client.blockchain.get_address(
    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    limit=10,
)
print(f"Total recibido: {info['total_received'] / 1e8} BTC")
```

### `get_multi_address(addresses, *, limit=50, offset=0)`

Obtiene información de múltiples direcciones (o xpubs) a la vez.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `addresses` | `list[str]` | Lista de direcciones o xpubs |
| `limit` | `int` | Nº de transacciones (máx 100) |
| `offset` | `int` | Saltar las primeras N transacciones |

**Retorna:** `MultiAddressResponse`

```python
multi = await client.blockchain.get_multi_address(["addr1", "addr2"])
for addr in multi.addresses:
    print(f"{addr.address}: {addr.final_balance / 1e8} BTC")
```

## Balance

### `get_balance(addresses)`

Obtiene el balance de una o más direcciones.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `addresses` | `list[str]` | Lista de direcciones |

**Retorna:** `dict[str, dict[str, int]]`

```python
balances = await client.blockchain.get_balance(["addr1", "addr2"])
# Retorna: {"addr1": {"final_balance": 50000, "n_tx": 10, ...}, ...}
```

## UTXOs

### `get_unspent_outputs(addresses, *, limit=250, confirmations=None)`

Obtiene los outputs no gastados (UTXOs).

| Parámetro | Tipo | Descripción |
|---|---|---|
| `addresses` | `list[str]` | Lista de direcciones |
| `limit` | `int` | Nº de UTXOs (máx 1000) |
| `confirmations` | `int` | Mínimo de confirmaciones requeridas |

**Retorna:** `list[UnspentOutput]`

```python
utxos = await client.blockchain.get_unspent_outputs(
    ["addr1"],
    limit=100,
    confirmations=6,
)
for utxo in utxos:
    print(f"TX: {utxo.tx_hash}, Valor: {utxo.value / 1e8} BTC")
```

