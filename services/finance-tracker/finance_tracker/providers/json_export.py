from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from dateutil import parser as date_parser

from .base import FinanceProvider

_PAYEE_KEYS = (
    "payee",
    "description",
    "merchant",
    "merchantName",
    "merchant_name",
    "counterparty",
    "counterpartyName",
    "business_name",
    "title",
    "memo",
    "details",
    "תיאור",
)
_AMOUNT_KEYS = ("amount", "sum", "value", "debit", "credit", "סכום", "total")
_DATE_KEYS = (
    "date",
    "transaction_date",
    "transactionDate",
    "booking_date",
    "bookingDate",
    "bookedAt",
    "valueDate",
    "value_date",
    "posted_at",
    "created_at",
    "תאריך",
)
_NON_TX_SIGNATURE_KEYS = frozenset(
    {"login", "role", "tfa_enabled", "tfa_level", "organization_roles_count", "saml_name_id"}
)


def _first_value(row: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def _looks_like_transaction(row: dict[str, Any]) -> bool:
    if not isinstance(row, dict):
        return False
    if _NON_TX_SIGNATURE_KEYS.intersection(row.keys()):
        return False
    has_amount = _first_value(row, _AMOUNT_KEYS) is not None
    has_date = _first_value(row, _DATE_KEYS) is not None
    has_payee = _first_value(row, _PAYEE_KEYS) is not None
    return has_amount or (has_date and has_payee)


def _parse_date(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        ts = float(value)
        if ts > 1e12:
            ts /= 1000.0
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    try:
        dt = date_parser.parse(str(value))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError):
        return None


def _extract_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if not isinstance(data, dict):
        return []
    for key in ("transactions", "items", "records", "data"):
        value = data.get(key)
        if isinstance(value, list):
            return [r for r in value if isinstance(r, dict)]
        if isinstance(value, dict):
            nested = _extract_rows(value)
            if nested:
                return nested
    return []


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "json_export",
        "payee": str(_first_value(row, _PAYEE_KEYS) or ""),
        "amount": _first_value(row, _AMOUNT_KEYS) or "0",
        "date": _first_value(row, _DATE_KEYS) or "",
        "raw": row,
    }


class JsonExportProvider(FinanceProvider):
    """Ingest Moneytor or bank JSON exports (path B2 in plan)."""

    def __init__(self, json_path: Path) -> None:
        self.json_path = json_path

    def fetch_transactions(self, since_days: int = 30) -> list[dict[str, Any]]:
        if not self.json_path.exists():
            return []
        try:
            data = json.loads(self.json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

        cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
        rows: list[dict[str, Any]] = []
        for row in _extract_rows(data):
            if not _looks_like_transaction(row):
                continue
            normalized = _normalize_row(row)
            tx_date = _parse_date(normalized.get("date"))
            if tx_date is not None and tx_date < cutoff:
                continue
            rows.append(normalized)
        return rows

    def fetch_balances(self) -> list[dict[str, Any]]:
        if not self.json_path.exists():
            return []
        try:
            data = json.loads(self.json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        if isinstance(data, dict):
            balances = data.get("balances")
            if isinstance(balances, list):
                return balances
        return []
