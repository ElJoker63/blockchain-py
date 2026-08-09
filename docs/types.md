# Tipos de Datos

Todos los tipos son `dataclass` congelados (inmutables) definidos en `blockchain.types`.

---

## Block

Bloque de Bitcoin completo.

```python
@dataclass(frozen=True)
class Block:
    hash: str = ""
    version: int = 0
    previous_block: str = ""
    merkle_root: str = ""
    time: int = 0
    bits: str = ""
    height: int = 0
    nonce: int = 0
    size: int = 0
    difficulty: float = 0.0
    tx: list[dict[str, Any]] = field(default_factory=list)
```

---

## BlockHeight

Resultado de consultar bloques por altura.

```python
@dataclass(frozen=True)
class BlockHeight:
    blocks: list[dict[str, Any]] = field(default_factory=list)
```

---

## LatestBlock

Resumen del último bloque de la cadena.

```python
@dataclass(frozen=True)
class LatestBlock:
    hash: str = ""
    time: int = 0
    block_index: int = 0
    height: int = 0
    txIndexes: int = 0
```

---

## Transaction

Transacción completa de Bitcoin.

```python
@dataclass(frozen=True)
class Transaction:
    hash: str = ""
    ver: int = 0
    vin_sz: int = 0
    vout_sz: int = 0
    size: int = 0
    weight: int = 0
    fee: int = 0
    time: int = 0
    block_height: int = 0
    block_hash: str = ""
    inputs: list[dict[str, Any]] = field(default_factory=list)
    out: list[dict[str, Any]] = field(default_factory=list)
```

---

## TransactionInput

Input individual de una transacción.

```python
@dataclass(frozen=True)
class TransactionInput:
    prev_out: dict[str, Any] = field(default_factory=dict)
    script: str = ""
    sequence: int = 0
    witness: str = ""
```

---

## TransactionOutput

Output individual de una transacción.

```python
@dataclass(frozen=True)
class TransactionOutput:
    value: int = 0
    script: str = ""
    addr: str = ""
```

---

## AddressInfo

Información resumida de una dirección Bitcoin.

```python
@dataclass(frozen=True)
class AddressInfo:
    address: str = ""
    hash160: str = ""
    n_tx: int = 0
    total_received: int = 0
    total_sent: int = 0
    final_balance: int = 0
```

---

## Balance

Resultado de balance para una dirección.

```python
@dataclass(frozen=True)
class Balance:
    final_balance: int = 0
    n_tx: int = 0
    total_received: int = 0
    total_sent: int = 0
```

---

## MultiAddressInfo

Información de una dirección en respuesta multi-dirección.

```python
@dataclass(frozen=True)
class MultiAddressInfo:
    address: str = ""
    hash160: str = ""
    n_tx: int = 0
    total_received: int = 0
    total_sent: int = 0
    final_balance: int = 0
```

---

## MultiAddressResponse

Respuesta de consulta multi-dirección.

```python
@dataclass(frozen=True)
class MultiAddressResponse:
    addresses: list[MultiAddressInfo] = field(default_factory=list)
    txs: list[dict[str, Any]] = field(default_factory=list)
```

---

## UnspentOutput

Output no gastado (UTXO).

```python
@dataclass(frozen=True)
class UnspentOutput:
    tx_hash: str = ""
    tx_hash_big_endian: str = ""
    tx_index: int = 0
    tx_output_n: int = 0
    script: str = ""
    value: int = 0
    value_hex: str = ""
    confirmations: int = 0
```

!!! note "Orden del hash"
    `tx_hash` viene en orden de bytes invertido. Usa `tx_hash_big_endian` para el hash estándar.

---

## UnconfirmedTransaction

Transacción pendiente (mempool).

```python
@dataclass(frozen=True)
class UnconfirmedTransaction:
    hash: str = ""
    time: int = 0
    ver: int = 0
    vin_sz: int = 0
    vout_sz: int = 0
    size: int = 0
    weight: int = 0
    fee: int = 0
    inputs: list[dict[str, Any]] = field(default_factory=list)
    out: list[dict[str, Any]] = field(default_factory=list)
```

---

## ChartData

Respuesta de la API de gráficas.

```python
@dataclass(frozen=True)
class ChartData:
    status: str = ""
    name: str = ""
    unit: str = ""
    period: str = ""
    description: str = ""
    values: list[ChartValue] = field(default_factory=list)
```

---

## ChartValue

Punto individual de datos en una gráfica.

```python
@dataclass(frozen=True)
class ChartValue:
    x: int = 0     # Timestamp Unix
    y: float = 0.0  # Valor del dato
```

---

## Ticker

Ticker completo con todas las divisas.

```python
@dataclass(frozen=True)
class Ticker:
    currencies: dict[str, TickerCurrency] = field(default_factory=dict)
```

---

## TickerCurrency

Datos del ticker para una moneda individual.

```python
@dataclass(frozen=True)
class TickerCurrency:
    fifteen_min: float = 0.0  # Precio retrasado 15min
    last: float = 0.0         # Último precio
    buy: float = 0.0          # Precio de compra
    sell: float = 0.0         # Precio de venta
    symbol: str = ""          # Símbolo (ej: "$")
```

---

## ExchangeRate

Tasa de cambio simplificada.

```python
@dataclass(frozen=True)
class ExchangeRate:
    currency: str = ""
    fifteen_min: float = 0.0
    last: float = 0.0
    buy: float = 0.0
    sell: float = 0.0
    symbol: str = ""
```

---

## SimpleQueryResult

Resultado de la Simple Query API (texto plano parseado).

```python
@dataclass(frozen=True)
class SimpleQueryResult:
    endpoint: str = ""
    value: Any = None  # int, float, o str
```

---

<p align="center">
  Desarrollado con ❤️ por <strong>ElJoker63</strong><br>
  <em>&lt;☕&gt;+☕️=❤️</em>
</p>
