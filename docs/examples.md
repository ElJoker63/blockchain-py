# Ejemplos

Ejemplos prácticos de uso de la librería.

---

## Monitoreo de dirección en tiempo real

Detecta cuando una dirección recibe fondos:

```python
import asyncio
from blockchain import BlockchainClient

TARGET_ADDR = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

async def on_tx(tx: dict):
    for output in tx.get("out", []):
        if output.get("addr") == TARGET_ADDR:
            btc = output["value"] / 1e8
            print(f"¡Recibido! {btc:.8f} BTC")

async def main():
    async with BlockchainClient() as client:
        ws = client.websocket()
        ws.on_transaction(on_tx)
        await ws.connect()
        await ws.subscribe_address(TARGET_ADDR)
        await ws.run_forever()

asyncio.run(main())
```

---

## Dashboard de métricas de la red

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        # Datos actuales
        difficulty = await client.simple.get_difficulty()
        hashrate = await client.simple.get_hashrate()
        block_count = await client.simple.get_block_count()
        price = await client.simple.get_24hr_price()
        market_cap = await client.simple.get_market_cap()
        tx_count = await client.simple.get_24hr_tx_count()

        print("═══════════════════════════════════")
        print("      DASHBOARD BITCOIN")
        print("═══════════════════════════════════")
        print(f"  Bloque:        #{block_count.value:,}")
        print(f"  Dificultad:    {difficulty.value:,.0f}")
        print(f"  Hash rate:     {hashrate.value} GH/s")
        print(f"  Precio:        ${price.value:,.2f}")
        print(f"  Market cap:    ${market_cap.value:,.0f}")
        print(f"  Tx/24h:        {tx_count.value:,}")
        print("═══════════════════════════════════")

asyncio.run(main())
```

---

## Análisis de dirección

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

    async with BlockchainClient() as client:
        balance = await client.blockchain.get_balance([addr])
        info = balance[addr]

        received = await client.simple.get_received_by_address(addr)
        sent = await client.simple.get_sent_by_address(addr)

        print(f"Dirección: {addr}")
        print(f"Balance:   {info['final_balance'] / 1e8:.8f} BTC")
        print(f"Recibido:  {received.value / 1e8:.8f} BTC")
        print(f"Enviado:   {sent.value / 1e8:.8f} BTC")
        print(f"Tx count:  {info['n_tx']:,}")

asyncio.run(main())
```

---

## Gráfica de precio y estadísticas

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        # Precio último año
        price = await client.charts.get_chart(
            "bitcoin-price",
            timespan="1year",
            rolling_average="8hours",
        )
        prices = [p.y for p in price.values]
        print(f"Precio (1 año):")
        print(f"  Mín: ${min(prices):,.2f}")
        print(f"  Máx: ${max(prices):,.2f}")
        print(f"  Avg: ${sum(prices)/len(prices):,.2f}")

        # Transacciones últimos 7 días
        tx = await client.charts.get_chart(
            "n-transactions",
            timespan="7days",
        )
        tx_vals = [p.y for p in tx.values]
        print(f"\nTransacciones (7 días):")
        print(f"  Total: {sum(tx_vals):,.0f}")
        print(f"  Promedio/día: {sum(tx_vals)/7:,.0f}")

asyncio.run(main())
```

---

## Comparar múltiples direcciones

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    addrs = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
    ]

    async with BlockchainClient() as client:
        multi = await client.blockchain.get_multi_address(addrs)

        print("Comparación de direcciones:")
        print("-" * 50)
        for addr in multi.addresses:
            print(f"  {addr.address}")
            print(f"    Balance: {addr.final_balance / 1e8:.8f} BTC")
            print(f"    Tx: {addr.n_tx:,}")
            print()

asyncio.run(main())
```

---

## Seguimiento de bloques nuevos

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        print("Esperando nuevos bloques...")
        print("Presiona Ctrl+C para salir\n")

        ws = client.websocket()

        async def on_block(block: dict):
            h = block.get("height", "?")
            hash_ = block.get("hash", "?")[:20]
            print(f"🧱 Bloque #{h}: {hash_}...")

        ws.on_block(on_block)
        await ws.connect()
        await ws.subscribe_new_blocks()
        await ws.run_forever()

asyncio.run(main())
```

---

## Exportar datos de gráficas a CSV

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        csv = await client.charts.get_chart_raw(
            "bitcoin-price",
            timespan="3months",
        )

        with open("btc_price_3m.csv", "w") as f:
            f.write(csv)

        print("Datos exportados a btc_price_3m.csv")

asyncio.run(main())
```

---

## Verificar si una transacción fue rechazada

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    tx_hash = "some_hash_here"

    async with BlockchainClient() as client:
        result = await client.simple.get_rejected(tx_hash)
        if result.value == "No information available about this hash":
            print("Transacción válida o aún no procesada")
        else:
            print(f"Rechazada: {result.value}")

asyncio.run(main())
```

---

<p align="center">
  Desarrollado con ❤️ por <strong>ElJoker63</strong><br>
  <em>&lt;☕&gt;+☕️=❤️</em>
</p>
