# Simple Query API

Endpoints de texto plano para estadísticas rápidas de la red Bitcoin.

```python
api = client.simple
```

!!! warning "Rate Limit"
    Máximo **1 petición cada 10 segundos**. Todos los valores de BTC están en **Satoshi** (dividir por 100,000,000 para obtener BTC).

Todos los métodos retornan `SimpleQueryResult` con los campos `endpoint` y `value` (auto-parseado a `int`, `float` o `str`).

---

## Estadísticas de Red

### `get_difficulty()`

Dificultad actual del target como decimal.

```python
result = await client.simple.get_difficulty()
print(f"Dificultad: {result.value}")
```

---

### `get_block_count()`

Altura actual del bloque más largo.

```python
result = await client.simple.get_block_count()
print(f"Bloques: {result.value}")
```

---

### `get_latest_hash()`

Hash del último bloque.

```python
result = await client.simple.get_latest_hash()
print(f"Hash: {result.value}")
```

---

### `get_bc_per_block()`

Recompensa actual por bloque en BTC.

```python
result = await client.simple.get_bc_per_block()
print(f"Recompensa: {result.value} BTC")
```

---

### `get_total_bc()`

Total de BTC en circulación (retraso de hasta 1 hora). En Satoshi.

```python
result = await client.simple.get_total_bc()
print(f"Total: {result.value / 1e8:.8f} BTC")
```

---

### `get_probability()`

Probabilidad de encontrar un bloque válido por hash.

```python
result = await client.simple.get_probability()
print(f"Probabilidad: {result.value}")
```

---

### `get_hashes_to_win()`

Promedio de intentos de hash necesarios para resolver un bloque.

```python
result = await client.simple.get_hashes_to_win()
print(f"Hashes para ganar: {result.value}")
```

---

### `get_next_retarget()`

Altura del bloque del próximo ajuste de dificultad.

```python
result = await client.simple.get_next_retarget()
print(f"Próximo retarget: bloque #{result.value}")
```

---

### `get_avg_tx_size(blocks=None)`

Tamaño promedio de transacción para los últimos N bloques (default 1000).

```python
result = await client.simple.get_avg_tx_size(2000)
print(f"Tamaño promedio: {result.value} bytes")
```

---

### `get_avg_tx_value(blocks=None)`

Valor promedio de transacción para los últimos N bloques (default 1000).

```python
result = await client.simple.get_avg_tx_value()
print(f"Valor promedio: {result.value} Satoshi")
```

---

### `get_interval()`

Tiempo promedio entre bloques en segundos.

```python
result = await client.simple.get_interval()
print(f"Intervalo: {result.value} segundos")
```

---

### `get_eta()`

Tiempo estimado hasta el siguiente bloque (segundos).

```python
result = await client.simple.get_eta()
print(f"ETA: {result.value} segundos")
```

---

### `get_avg_tx_number(blocks=None)`

Promedio de transacciones por bloque para los últimos N bloques (default 100).

```python
result = await client.simple.get_avg_tx_number(100)
print(f"Tx/bloque: {result.value}")
```

---

### `get_hashrate()`

Hash rate estimado de la red en gigahash.

```python
result = await client.simple.get_hashrate()
print(f"Hash rate: {result.value} GH/s")
```

---

## Consultas por Dirección

### `get_received_by_address(address)`

Total de BTC recibidos por una dirección.

```python
result = await client.simple.get_received_by_address("1A1z...")
print(f"Recibido: {result.value / 1e8} BTC")
```

---

### `get_sent_by_address(address)`

Total de BTC enviados por una dirección.

```python
result = await client.simple.get_sent_by_address("1A1z...")
print(f"Enviado: {result.value / 1e8} BTC")
```

---

### `get_address_balance(address)`

Balance de una dirección.

```python
result = await client.simple.get_address_balance("1A1z...")
print(f"Balance: {result.value / 1e8} BTC")
```

---

### `get_address_first_seen(address)`

Timestamp del bloque cuando la dirección fue vista por primera vez.

```python
result = await client.simple.get_address_first_seen("1A1z...")
print(f"Primera vez visto: {result.value}")
```

---

## Herramientas de Conversión

### `address_to_hash(address)`

Convierte una dirección Bitcoin a hash160.

```python
result = await client.simple.address_to_hash("1A1z...")
print(f"Hash160: {result.value}")
```

---

### `hash_to_address(hash160)`

Convierte un hash160 a dirección Bitcoin.

```python
result = await client.simple.hash_to_address("62e907b15cbf...")
print(f"Dirección: {result.value}")
```

---

### `hash_pubkey(pubkey)`

Convierte una clave pública a hash160.

```python
result = await client.simple.hash_pubkey("04...")
print(f"Hash: {result.value}")
```

---

### `addr_pubkey(pubkey)`

Convierte una clave pública a dirección Bitcoin.

```python
result = await client.simple.addr_pubkey("04...")
print(f"Dirección: {result.value}")
```

---

### `pubkey_addr(address)`

Convierte una dirección a clave pública (si está disponible).

```python
result = await client.simple.pubkey_addr("1A1z...")
print(f"Clave pública: {result.value}")
```

---

## Consultas de Transacciones

### `tx_total_btc_output(tx_hash)`

Valor total de outputs de una transacción.

```python
result = await client.simple.tx_total_btc_output("b6f699...")
print(f"Total output: {result.value / 1e8} BTC")
```

---

### `tx_total_btc_input(tx_hash)`

Valor total de inputs de una transacción.

```python
result = await client.simple.tx_total_btc_input("b6f699...")
print(f"Total input: {result.value / 1e8} BTC")
```

---

### `tx_fee(tx_hash)`

Comisión incluida en una transacción.

```python
result = await client.simple.tx_fee("b6f699...")
print(f"Fee: {result.value / 1e8} BTC")
```

---

### `tx_result(tx_hash, address)`

Resultado de una transacción enviada/recibida a una dirección.

```python
result = await client.simple.tx_result("b6f699...", "1A1z...")
print(f"Resultado: {result.value}")
```

---

## Datos de Mercado

### `get_24hr_price()`

Precio ponderado de 24 horas de los exchanges más grandes (USD).

```python
result = await client.simple.get_24hr_price()
print(f"Precio: ${result.value:,.2f}")
```

---

### `get_market_cap()`

Capitalización de mercado en USD.

```python
result = await client.simple.get_market_cap()
print(f"Market cap: ${result.value:,.0f}")
```

---

### `get_24hr_tx_count()`

Número de transacciones en las últimas 24 horas.

```python
result = await client.simple.get_24hr_tx_count()
print(f"Tx/24h: {result.value:,}")
```

---

### `get_24hr_btc_sent()`

BTC enviados en las últimas 24 horas.

```python
result = await client.simple.get_24hr_btc_sent()
print(f"BTC enviado: {result.value / 1e8:,.2f} BTC")
```

---

## Misceláneos

### `get_unconfirmed_count()`

Número de transacciones pendientes sin confirmar.

```python
result = await client.simple.get_unconfirmed_count()
print(f"Pendientes: {result.value}")
```

---

### `get_rejected(query)`

Razón por la que un hash de tx o bloque fue rechazado.

```python
result = await client.simple.get_rejected("tx_or_block_hash")
print(f"Razón: {result.value}")
```

---

<p align="center">
  Desarrollado con ❤️ por <strong>ElJoker63</strong><br>
  <em>&lt;☕&gt;+☕️=❤️</em>
</p>
