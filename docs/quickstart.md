# Inicio Rápido

## Conexión básica

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        # Tus consultas aquí
        pass

asyncio.run(main())
```

## Primer ejemplo completo

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        # 1. Último bloque
        block = await client.blockchain.get_latest_block()
        print(f"Último bloque: #{block.height}")

        # 2. Precio de Bitcoin
        ticker = await client.exchange.get_ticker()
        usd = ticker.currencies["USD"]
        print(f"BTC/USD: ${usd.last:,.2f}")

        # 3. Balance de una dirección
        addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Dirección de Satoshi
        balance = await client.blockchain.get_balance([addr])
        btc = balance[addr]["final_balance"] / 1e8
        print(f"Saldo: {btc:.8f} BTC")

        # 4. Dificultad actual
        difficulty = await client.simple.get_difficulty()
        print(f"Dificultad: {difficulty.value}")

asyncio.run(main())
```

**Salida:**

```
Último bloque: #961652
BTC/USD: $64,917.45
Saldo: 72.77441127 BTC
Dificultad: 110454481734366.7
```

## Conectarse a WebSocket en tiempo real

```python
import asyncio
from blockchain import BlockchainClient

async def on_block(block: dict):
    print(f"Nuevo bloque #{block['height']}: {block['hash'][:20]}...")

async def on_tx(tx: dict):
    total = sum(o["value"] for o in tx.get("out", []))
    print(f"Tx {tx['hash'][:16]}... = {total / 1e8:.8f} BTC")

async def main():
    async with BlockchainClient() as client:
        ws = client.websocket()
        ws.on_block(on_block)
        ws.on_transaction(on_tx)

        await ws.connect()
        await ws.subscribe_new_blocks()
        await ws.subscribe_unconfirmed_transactions()

        # Ejecutar 30 segundos
        task = await ws.start_background()
        await asyncio.sleep(30)
        await ws.close()

asyncio.run(main())
```

## Obtener datos de gráficas

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        chart = await client.charts.get_chart(
            "bitcoin-price",
            timespan="1year",
            rolling_average="8hours",
        )
        print(f"{chart.name}: {len(chart.values)} puntos")
        for point in chart.values[:3]:
            print(f"  {point.x}: ${point.y:,.2f}")

asyncio.run(main())
```

## Convertir fiat a BTC

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        btc = await client.exchange.to_btc("EUR", 1000)
        print(f"1,000 EUR = {btc:.8f} BTC")

asyncio.run(main())
```

---

<p align="center">
  Desarrollado con ❤️ por <strong>ElJoker63</strong><br>
  <em>&lt;☕&gt;+☕️=❤️</em>
</p>
