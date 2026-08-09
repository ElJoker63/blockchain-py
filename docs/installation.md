# Instalación

## Requisitos previos

- Python 3.10 o superior
- pip

## Instalar desde PyPI

```bash
pip install blockchain-api
```

## Instalar la última versión de desarrollo

```bash
pip install git+https://github.com/ElJoker63/blockchain-py.git
```

## Instalar en modo desarrollo (para contribuir)

```bash
git clone https://github.com/ElJoker63/blockchain-py.git
cd blockchain-py
pip install -e .
```

## Verificar la instalación

```python
import blockchain
print(blockchain.__version__)  # 1.0.0
```

## Dependencias

| Paquete | Versión | Uso |
|---|---|---|
| `httpx` | ≥ 0.27 | Cliente HTTP asincrónico |
| `websockets` | ≥ 13.0 | Conexiones WebSocket |

