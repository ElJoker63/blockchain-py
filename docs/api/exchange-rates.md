# Exchange Rates API

Datos de ticker y conversión de divisas para Bitcoin.

```python
api = client.exchange
```

---

## `get_ticker()`

Obtiene el ticker completo con todas las divisas soportadas.

**Retorna:** `Ticker` — un diccionario de códigos ISO-4217 → `TickerCurrency`

```python
ticker = await client.exchange.get_ticker()

for code, data in ticker.currencies.items():
    print(f"{code}: {data.symbol}{data.last:,.2f}")
```

### Cada `TickerCurrency` contiene:

| Campo | Tipo | Descripción |
|---|---|---|
| `fifteen_min` | `float` | Precio retrasado 15 minutos |
| `last` | `float` | Último precio de mercado |
| `buy` | `float` | Precio de compra |
| `sell` | `float` | Precio de venta |
| `symbol` | `str` | Símbolo de la moneda (ej: `$`) |

### Ejemplo con divisas específicas

```python
ticker = await client.exchange.get_ticker()
usd = ticker.currencies["USD"]
eur = ticker.currencies["EUR"]
gbp = ticker.currencies["GBP"]

print(f"USD: ${usd.last:,.2f}")
print(f"EUR: €{eur.last:,.2f}")
print(f"GBP: £{gbp.last:,.2f}")
```

---

## `get_exchange_rate(currency)`

Obtiene el ticker para una sola moneda.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `currency` | `str` | Código ISO-4217 (ej: `"USD"`, `"EUR"`) |

**Retorna:** `ExchangeRate`

```python
rate = await client.exchange.get_exchange_rate("USD")
print(f"Último: ${rate.last:,.2f}")
print(f"Compra: ${rate.buy:,.2f}")
print(f"Venta:  ${rate.sell:,.2f}")
```

!!! error "ValueError"
    Se lanza `ValueError` si la moneda no es soportada.

---

## `to_btc(currency, value)`

Convierte una cantidad en moneda fiduciaria a Bitcoin.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `currency` | `str` | Código ISO-4217 |
| `value` | `float` | Cantidad en la moneda dada |

**Retorna:** `float` — Cantidad equivalente en BTC

```python
btc = await client.exchange.to_btc("USD", 1000)
print(f"$1,000 = {btc:.8f} BTC")

btc = await client.exchange.to_btc("EUR", 500)
print(f"€500 = {btc:.8f} BTC")
```

---

## Ejemplo completo

```python
import asyncio
from blockchain import BlockchainClient

async def main():
    async with BlockchainClient() as client:
        ticker = await client.exchange.get_ticker()

        print("Precios de Bitcoin:")
        print("-" * 40)
        for code in ["USD", "EUR", "GBP", "JPY", "CNY"]:
            if code in ticker.currencies:
                c = ticker.currencies[code]
                print(f"  {code}: {c.symbol}{c.last:,.2f}")

        print()
        btc = await client.exchange.to_btc("USD", 10000)
        print(f"$10,000 = {btc:.8f} BTC")

asyncio.run(main())
```

---

<p align="center">
  Desarrollado con ❤️ por <strong>ElJoker63</strong><br>
  <em>&lt;☕&gt;+☕️=❤️</em>
</p>
