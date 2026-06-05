from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx

from .base import FinanceProvider
from .csv_export import CsvExportProvider
from .json_export import JsonExportProvider


class MoneytorProvider(FinanceProvider):
    """
    Moneytor integration (read-only).
    Path A: MONEYTOR_API_URL + MONEYTOR_API_KEY when available.
    Path B: MONEYTOR_JSON_EXPORT or MONEYTOR_CSV_EXPORT fallback.
    """

    def __init__(self) -> None:
        self.api_url = os.environ.get("MONEYTOR_API_URL", "").rstrip("/")
        self.api_key = os.environ.get("MONEYTOR_API_KEY", "")
        json_path = os.environ.get("MONEYTOR_JSON_EXPORT", "")
        csv_path = os.environ.get("MONEYTOR_CSV_EXPORT", "")
        self._json = JsonExportProvider(Path(json_path)) if json_path else None
        self._csv = CsvExportProvider(Path(csv_path)) if csv_path else None

    def fetch_transactions(self, since_days: int = 30) -> list[dict[str, Any]]:
        if self.api_url and self.api_key:
            try:
                r = httpx.get(
                    f"{self.api_url}/transactions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    params={"days": since_days},
                    timeout=30.0,
                )
                if r.status_code == 200:
                    data = r.json()
                    return data if isinstance(data, list) else data.get("transactions", [])
            except httpx.HTTPError:
                pass
        if self._json:
            txs = self._json.fetch_transactions(since_days=since_days)
            if txs:
                return txs
        if self._csv:
            return self._csv.fetch_transactions(since_days=since_days)
        return []

    def fetch_balances(self) -> list[dict[str, Any]]:
        if self.api_url and self.api_key:
            try:
                r = httpx.get(
                    f"{self.api_url}/balances",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0,
                )
                if r.status_code == 200:
                    data = r.json()
                    return data if isinstance(data, list) else data.get("balances", [])
            except httpx.HTTPError:
                pass
        if self._json:
            balances = self._json.fetch_balances()
            if balances:
                return balances
        return []
