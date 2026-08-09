"""Charts & Statistics API — historical data feeds."""

from __future__ import annotations

from typing import Any

from blockchain._http import HTTPClient
from blockchain.types import ChartData


class ChartsAPI:
    """Async wrapper for the Blockchain.com Charts API.

    The Charts API returns historical data in JSON or CSV format.
    """

    BASE_URL = "https://api.blockchain.info"
    CHART_NAMES: set[str] = {
        "avg-bc-transaction-size",
        "avg-confirmation-time",
        "avg-tx-value",
        "avg-transaction-size",
        "bitcoin-fees-usd",
        "bitcoin-hash-rate",
        "bitcoin-market-cap",
        "bitcoin-price",
        "bitcoin-transaction-fees-usd",
        "bitcoin-transaction-fees-usd-per-n-byte",
        "bitcoin-volatility",
        "blocks-size",
        "btc-block-reward",
        "btc-mined",
        "btc-to-usd",
        "calc-tx-fee-volatility",
        "confirmation-time",
        "cost-per-transaction",
        "cost-per-transaction-percent",
        "difficulty",
        "hash-rate",
        "median-confirmation-time",
        "market-cap",
        "miners-revenue",
        "miners-revenue-per-gh",
        "miners-revenue-usd",
        "my-wallet-n-users",
        "n-unique-addresses",
        "n-transactions",
        "n-transactions-per-block",
        "n-unique-spending-addresses",
        "n-vs-7d-avg-merchants",
        "n-merchants",
        "n-output-spending-coins-per-day",
        "n-output-spending-coins-per-sec",
        "n-spending-output-type",
        "n-spending-output-type-p2pkh",
        "n-spending-output-type-p2ms",
        "n-spending-output-type-p2sh",
        "n-spending-output-type-p2pk",
        "n-spending-output-type-other",
        "n-spending-output-type-nonstandard",
        "n-spending-output-type-p2wpkh",
        "n-spending-output-type-p2wsh",
        "n-transactions-mempool-per-block",
        "n-confirmed-tx-per-day",
        "n-unconfirmed-tx-per-day",
        "n-unconfirmed-tx",
        "n-output-type",
        "n-output-type-p2pkh",
        "n-output-type-p2ms",
        "n-output-type-p2sh",
        "n-output-type-p2pk",
        "n-output-type-other",
        "n-output-type-nonstandard",
        "n-output-type-p2wpkh",
        "n-output-type-p2wsh",
        "n-output-type-p2tr",
        "market-price",
        "output-volume",
        "peers",
        "pizza-bought-for-btc",
        "realized-cap",
        "revenue-usd",
        "trade-volume",
        "transactions-per-second",
        "treasury-balance",
        "unclassified-output-volume",
        "utxo-count",
        "utxo-value-avg",
        "utxo-value-median",
        "utxo-value-mean",
        "utxo-count-value-100m-usd",
        "utxo-count-value-1-1-btc",
        "utxo-count-value-1-10-btc",
        "utxo-count-value-10-100-btc",
        "utxo-count-value-100-1k-btc",
        "utxo-count-value-1k-10k-btc",
        "utxo-count-value-10k-btc",
    }

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    async def get_chart(
        self,
        chart_name: str,
        *,
        timespan: str | None = None,
        rolling_average: str | None = None,
        start: str | None = None,
        format: str = "json",
        sampled: bool = True,
    ) -> ChartData:
        """Fetch chart data from the Charts API.

        Parameters
        ----------
        chart_name:
            The chart identifier (e.g. ``"bitcoin-price"``).
        timespan:
            Duration of data, e.g. ``"5weeks"``, ``"1year"``, ``"3months"``.
        rolling_average:
            Rolling average window, e.g. ``"8hours"``.
        start:
            Start datetime as ``YYYY-MM-DD`` or ``YYYY-MM-DDThh:mm:ss`` (UTC).
        format:
            ``"json"`` (default) or ``"csv"``.
        sampled:
            When *True* (default) limits datapoints to ~1500 for performance.
        """
        params: dict[str, str | bool] = {"format": format, "sampled": sampled}
        if timespan:
            params["timespan"] = timespan
        if rolling_average:
            params["rollingAverage"] = rolling_average
        if start:
            params["start"] = start
        data = await self._http.get_json_from(
            self.BASE_URL, f"/charts/{chart_name}", params=params
        )
        return ChartData.from_dict(data)

    async def get_chart_raw(
        self,
        chart_name: str,
        *,
        timespan: str | None = None,
        rolling_average: str | None = None,
        start: str | None = None,
        sampled: bool = True,
    ) -> str:
        """Fetch chart data as raw CSV text.

        Parameters are identical to :meth:`get_chart`.
        """
        params: dict[str, str | bool] = {"format": "csv", "sampled": sampled}
        if timespan:
            params["timespan"] = timespan
        if rolling_average:
            params["rollingAverage"] = rolling_average
        if start:
            params["start"] = start
        return await self._http.get_text_from(
            self.BASE_URL, f"/charts/{chart_name}", params=params
        )

    def list_available_charts(self) -> list[str]:
        """Return the list of known chart name identifiers."""
        return sorted(self.CHART_NAMES)
