# Cliente

El `BlockchainClient` es el punto de entrada principal. Propor acceso a todas las sub-APIs y gestiona las conexiones HTTP.

## Uso básico

```python
from blockchain import BlockchainClient

async with BlockchainClient() as client:
    # client.blockchain  → Blockchain Data API
    # client.simple      → Simple Query API
    # client.exchange    → Exchange Rates API
    # client.charts      → Charts API
    # client.websocket() → WebSocket streaming
    pass
```

## Parámetros del constructor

| Parámetro | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `timeout` | `float` | `30.0` | Timeout de peticiones HTTP en segundos |
| `headers` | `dict` | `None` | Headers HTTP extra para todas las peticiones |
| `max_connections` | `int` | `20` | Tamaño del pool de conexiones |
| `max_keepalive` | `int` | `10` | Tamaño del pool de keep-alive |

### Ejemplo con configuración personalizada

```python
async with BlockchainClient(
    timeout=60.0,
    headers={"X-Custom": "value"},
    max_connections=50,
) as client:
    ...
```

## Sub-APIs disponibles

| Atributo | Tipo | Descripción |
|---|---|---|
| `client.blockchain` | `BlockchainAPI` | Bloques, transacciones, direcciones, UTXOs |
| `client.simple` | `SimpleQueryAPI` | Endpoints de texto plano |
| `client.exchange` | `ExchangeRatesAPI` | Ticker y conversión de divisas |
| `client.charts` | `ChartsAPI` | Datos históricos y gráficas |

## Método `websocket()`

Crea un nuevo cliente WebSocket para eventos en tiempo real:

```python
ws = client.websocket()

# O con URL personalizada
ws = client.websocket(url="wss://otro-servidor.com/ws")
```

## Método `close()`

Cierra todas las conexiones HTTP subyacentes:

```python
await client.close()
```

!!! note "Context Manager"
    Cuando usas `async with BlockchainClient()`, el cierre automático se ejecuta al salir del bloque.

---

<p align="center">
  Desarrollado con ❤️ por <strong>ElJoker63</strong><br>
  <em>&lt;☕&gt;+☕️=❤️</em>
</p>
