# Charts & Statistics API

Datos históricos y gráficas de la red Bitcoin.

```python
api = client.charts
```

## `get_chart(chart_name, **options)`

Obtiene datos de una gráfica en formato JSON.

### Parámetros

| Parámetro | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `chart_name` | `str` | *requerido* | Identificador de la gráfica |
| `timespan` | `str` | `None` | Duración: `"5weeks"`, `"1year"`, `"3months"` |
| `rolling_average` | `str` | `None` | Ventana de promediado: `"8hours"` |
| `start` | `str` | `None` | Fecha inicio: `"YYYY-MM-DD"` o `"YYYY-MM-DDThh:mm:ss"` |
| `format` | `str` | `"json"` | `"json"` o `"csv"` |
| `sampled` | `bool` | `True` | Limitar a ~1500 puntos de datos |

**Retorna:** `ChartData`

### Ejemplo

```python
chart = await client.charts.get_chart(
    "bitcoin-price",
    timespan="5years",
    rolling_average="8hours",
    sampled=True,
)

print(f"Nombre: {chart.name}")
print(f"Unidad: {chart.unit}")
print(f"Descripción: {chart.description}")
print(f"Período: {chart.period}")
print(f"Puntos de datos: {len(chart.values)}")

for point in chart.values[:5]:
    print(f"  {point.x}: ${point.y:,.2f}")
```

## `get_chart_raw(chart_name, **options)`

Obtiene datos de una gráfica como texto CSV puro.

### Parámetros

Mismos que `get_chart` excepto que el formato siempre es CSV.

**Retorna:** `str` — CSV con formato `YYYY-MM-DD HH:MM:SS,value`

```python
csv_data = await client.charts.get_chart_raw(
    "n-transactions",
    timespan="3months",
)
print(csv_data)
```

## `list_available_charts()`

Retorna la lista de identificadores de gráficas disponibles.

**Retorna:** `list[str]`

```python
charts = client.charts.list_available_charts()
print(f"Gráficas disponibles: {len(charts)}")
for name in charts:
    print(f"  - {name}")
```

## Gráficas disponibles

| Identificador | Descripción |
|---|---|
| `bitcoin-price` | Precio de Bitcoin |
| `market-cap` | Capitalización de mercado |
| `trade-volume` | Volumen de trading |
| `bitcoin-hash-rate` | Hash rate de la red |
| `difficulty` | Dificultad de minería |
| `bitcoin-volatility` | Volatilidad del precio |
| `n-transactions` | Número de transacciones |
| `n-unique-addresses` | Direcciones únicas |
| `n-transactions-per-block` | Tx por bloque |
| `transactions-per-second` | Transacciones por segundo |
| `avg-confirmation-time` | Tiempo promedio de confirmación |
| `miners-revenue` | Ingresos de mineros |
| `miners-revenue-usd` | Ingresos de mineros (USD) |
| `btc-mined` | BTC minados |
| `btc-block-reward` | Recompensa por bloque |
| `blocks-size` | Tamaño de los bloques |
| `cost-per-transaction` | Costo por transacción |
| `hash-rate` | Hash rate |
| `my-wallet-n-usd` | Usuarios de wallets |
| `n-output-type-*` | Tipos de output |
| `n-spending-output-type-*` | Tipos de gasto |
| `utxo-count` | Cantidad de UTXOs |
| `utxo-value-*` | Valor de UTXOs por rango |
| ... | *y más* |

!!! tip
    Usa `list_available_charts()` para obtener la lista completa actualizada.

## Ejemplo completo

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        # Precio de los últimos 3 meses
        price_chart = await client.charts.get_chart(
            "bitcoin-price",
            timespan="3months",
            rolling_average="8hours",
        )

        prices = [p.y for p in price_chart.values]
        print(f"Precio mínimo: ${min(prices):,.2f}")
        print(f"Precio máximo: ${max(prices):,.2f}")
        print(f"Precio promedio: ${sum(prices)/len(prices):,.2f}")

        # Transacciones diarias
        tx_chart = await client.charts.get_chart(
            "n-transactions",
            timespan="1month",
        )
        total = sum(p.y for p in tx_chart.values)
        print(f"Total tx (mes): {total:,.0f}")

asyncio.run(main())
```

