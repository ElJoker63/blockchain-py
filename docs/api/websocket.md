# WebSocket Streaming

Streaming en tiempo real de bloques y transacciones vía WebSocket.

```python
ws = client.websocket()
```

Se conecta a `wss://ws.blockchain.info/inv`.

## Conexión

### Como context manager

```python
async with client.websocket() as ws:
    ws.on_block(my_handler)
    await ws.connect()
    await ws.subscribe_new_blocks()
    await ws.run_forever()
```

### Manual

```python
ws = client.websocket()
await ws.connect()
# ... usar ...
await ws.close()
```

## Registro de handlers

### `on_block(handler)`

Registra un handler para eventos de nuevos bloques.

```python
async def on_block(block: dict):
    print(f"Nuevo bloque #{block['height']}: {block['hash'][:16]}...")

ws.on_block(on_block)
```

El handler recibe el payload `x` del mensaje WebSocket que contiene:

| Campo | Tipo | Descripción |
|---|---|---|
| `height` | `int` | Altura del bloque |
| `hash` | `str` | Hash del bloque |
| `mrklRoot` | `str` | Merkle root |
| `version` | `int` | Versión |
| `time` | `int` | Timestamp |
| `bits` | `str` | Bits |
| `nonce` | `int` | Nonce |

### `on_transaction(handler)`

Registra un handler para transacciones nuevas (de suscripciones a dirección).

```python
async def on_tx(tx: dict):
    total = sum(o["value"] for o in tx.get("out", []))
    print(f"Tx {tx['hash'][:16]}... = {total / 1e8:.8f} BTC")

ws.on_transaction(on_tx)
```

El handler recibe el payload `x` del mensaje que contiene:

| Campo | Tipo | Descripción |
|---|---|---|
| `hash` | `str` | Hash de la transacción |
| `inputs` | `list` | Lista de inputs |
| `out` | `list` | Lista de outputs (con `addr` y `value`) |
| `time` | `int` | Timestamp |

### `on_message(handler)`

Registra un handler para **todos** los mensajes (raw JSON).

```python
async def on_raw(msg: dict):
    print(f"OP: {msg.get('op')}")

ws.on_message(on_raw)
```

## Suscripciones

### Nuevos bloques

```python
await ws.subscribe_new_blocks()    # Suscribir
await ws.unsubscribe_new_blocks()  # Desuscribir
```

### Transacciones sin confirmar (mempool)

```python
await ws.subscribe_unconfirmed_transactions()    # Suscribir
await ws.unsubscribe_unconfirmed_transactions()  # Desuscribir
```

### Dirección específica

```python
await ws.subscribe_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
await ws.unsubscribe_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
```

## Pings

```python
await ws.ping()             # Keep-alive
await ws.ping_block()       # Solicitar último bloque
await ws.ping_transaction() # Solicitar última transacción
```

## Ejecución

### `run_forever()`

Bloquea hasta que la conexión se cierre.

```python
await ws.run_forever()
```

### `start_background()`

Inicia el loop de recepción como tarea de fondo.

```python
task = await ws.start_background()
# ... hacer otras cosas ...
await task  # o await ws.close()
```

## Ejemplo completo: monitoreo en tiempo real

```python
import asyncio
from blockchain import BlockchainClient

stats = {"blocks": 0, "txs": 0, "btc_moved": 0.0}

async def on_block(block: dict):
    stats["blocks"] += 1
    print(f"[BLOQUE #{block['height']}] Total: {stats['blocks']}")

async def on_tx(tx: dict):
    stats["txs"] += 1
    total = sum(o["value"] for o in tx.get("out", []))
    stats["btc_moved"] += total / 1e8
    if stats["txs"] % 10 == 0:
        print(f"[TX #{stats['txs']}] BTC movidos: {stats['btc_moved']:.4f}")

async def main():
    async with BlockchainClient() as client:
        ws = client.websocket()
        ws.on_block(on_block)
        ws.on_transaction(on_tx)

        await ws.connect()
        await ws.subscribe_new_blocks()
        await ws.subscribe_unconfirmed_transactions()

        print("Monitoreando blockchain en tiempo real...")
        await ws.run_forever()

asyncio.run(main())
```

## Ejemplo: alertas por dirección

```python
import asyncio
from blockchain import BlockchainClient

async def on_address_tx(tx: dict):
    addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    for output in tx.get("out", []):
        if output.get("addr") == addr:
            value = output["value"] / 1e8
            print(f"¡Recibido! {value:.8f} BTC en {addr}")

async def main():
    async with BlockchainClient() as client:
        ws = client.websocket()
        ws.on_transaction(on_address_tx)

        await ws.connect()
        await ws.subscribe_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

        await ws.run_forever()

asyncio.run(main())
```

