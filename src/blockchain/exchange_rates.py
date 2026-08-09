"""Exchange Rates API — ticker data and currency conversion."""

from __future__ import annotations

from blockchain._http import HTTPClient
from blockchain.types import ExchangeRate, Ticker


class ExchangeRatesAPI:
    """Async wrapper for the Blockchain.com Exchange Rates API."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    async def get_ticker(self) -> Ticker:
        """Fetch the full ticker with all supported currencies.

        Returns a :class:`Ticker` whose ``currencies`` dict maps
        ISO-4217 codes to :class:`TickerCurrency` objects.
        """
        data = await self._http.get_json("/ticker", params={"cors": "true"})
        return Ticker.from_dict(data)

    async def get_exchange_rate(self, currency: str) -> ExchangeRate:
        """Fetch the ticker for a single currency.

        Parameters
        ----------
        currency:
            ISO-4217 currency code, e.g. ``"USD"``, ``"EUR"``.
        """
        data = await self._http.get_json("/ticker", params={"cors": "true"})
        if currency not in data:
            raise ValueError(f"Unknown currency: {currency}")
        return ExchangeRate.from_dict(currency, data[currency])

    async def to_btc(self, currency: str, value: float) -> float:
        """Convert a fiat amount to Bitcoin.

        Parameters
        ----------
        currency:
            ISO-4217 currency code.
        value:
            The amount in the given currency.

        Returns
        -------
        float
            Equivalent amount in BTC.
        """
        raw = await self._http.get_text(
            "/tobtc",
            params={"currency": currency, "value": value},
        )
        return float(raw.strip())
