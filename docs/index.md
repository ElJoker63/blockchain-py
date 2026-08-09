# blockchain-api

<p align="center">
  <strong>Cliente Python asincrónico para la API de Blockchain.com Explorer</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/blockchain-api/"><img src="https://img.shields.io/pypi/v/blockchain-api?color=deep+orange&logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://pypi.org/project/blockchain-api/"><img src="https://img.shields.io/pypi/pyversions/blockchain-api?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/ElJoker63/blockchain-py/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/blockchain-api" alt="License"></a>
</p>

---

## ¿Qué es?

**blockchain-api** es una librería Python 100% asincrónica que envuelve cada endpoint de la [Blockchain.com Explorer API](https://www.blockchain.com/explorer/docs). Incluye:

- **Blockchain Data API** — bloques, transacciones, direcciones, UTXOs
- **Simple Query API** — estadísticas en texto plano
- **Exchange Rates API** — ticker y conversión de divisas
- **Charts API** — datos históricos y gráficas
- **WebSocket** — streaming en tiempo real de bloques y transacciones

## Características

| Característica | Descripción |
|---|---|
| 🔒 **100% async** | Construido sobre `httpx` y `websockets` |
| 📦 **Tipado completo** | 18 dataclasses tipadas con autocompletado en IDE |
| 🧩 **Modular** | Cada API es un módulo independiente |
| 🔄 **WebSocket** | Streaming en tiempo real con handlers de eventos |
| 📖 **Documentación completa** | MkDocs Material con ejemplos para cada endpoint |
| 🪶 **Ligero** | Solo depende de `httpx` y `websockets` |

## Instalación

```bash
pip install blockchain-api
```

## Uso rápido

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        # Último bloque
        block = await client.blockchain.get_latest_block()
        print(f"Bloque #{block.height}")

        # Precio actual
        ticker = await client.exchange.get_ticker()
        print(f"BTC/USD: ${ticker.currencies['USD'].last:,.2f}")

asyncio.run(main())
```

---

<p align="center">
  Desarrollado con ❤️ por <strong>ElJoker63</strong><br>
  <em>&lt;☕&gt;+☕️=❤️</em>
</p>
