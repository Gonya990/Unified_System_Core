from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .base import FinanceProvider


class CsvExportProvider(FinanceProvider):
    """Ingest Moneytor or bank CSV exports (path B in plan)."""

    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path

    def fetch_transactions(self, since_days: int = 30) -> list[dict[str, Any]]:
        if not self.csv_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        with open(self.csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(
                    {
                        "source": "csv_export",
                        "payee": row.get("payee") or row.get("description") or row.get("תיאור", ""),
                        "amount": row.get("amount") or row.get("סכום", "0"),
                        "date": row.get("date") or row.get("תאריך", ""),
                        "raw": row,
                    }
                )
        return rows

    def fetch_balances(self) -> list[dict[str, Any]]:
        return []
