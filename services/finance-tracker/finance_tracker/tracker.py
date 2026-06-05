from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .providers.moneytor import MoneytorProvider

STAGING_ROOT = Path(__file__).resolve().parents[3]
WIKI_DIR = STAGING_ROOT / "data" / "memory-wiki"
MANIFEST_PATH = STAGING_ROOT / "config" / "SOVEREIGN_MANIFEST.yaml"
DISPUTE_DIR = STAGING_ROOT / "templates" / "finance"


class FinanceTracker:
    def __init__(self, provider: MoneytorProvider | None = None) -> None:
        self.provider = provider or MoneytorProvider()
        self._whitelist = self._load_whitelist()

    def _load_whitelist(self) -> list[dict[str, Any]]:
        if not MANIFEST_PATH.exists():
            return []
        data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
        return (
            data.get("domains", {})
            .get("finance", {})
            .get("whitelist_recurring", [])
        )

    def _provenance(self) -> str:
        if os.environ.get("MONEYTOR_JSON_EXPORT"):
            return "moneytor_json_export"
        if os.environ.get("MONEYTOR_CSV_EXPORT"):
            return "moneytor_csv_export"
        if os.environ.get("MONEYTOR_API_URL") and os.environ.get("MONEYTOR_API_KEY"):
            return "moneytor_api"
        return "moneytor_csv_or_api"

    def _is_whitelisted(self, payee: str, amount: float) -> bool:
        for item in self._whitelist:
            pid = str(item.get("payee_id", ""))
            if pid and pid in payee.lower():
                max_amt = float(item.get("max_amount_ils", 999999))
                if amount <= max_amt:
                    return True
        return False

    def sync(self, since_days: int = 30) -> dict[str, Any]:
        WIKI_DIR.mkdir(parents=True, exist_ok=True)
        txs = self.provider.fetch_transactions(since_days=since_days)
        new_unknown = []
        for tx in txs:
            payee = str(tx.get("payee", ""))
            try:
                amount = float(str(tx.get("amount", "0")).replace(",", ""))
            except ValueError:
                amount = 0.0
            if self._is_whitelisted(payee, amount):
                continue
            entry_id = re.sub(r"[^a-zA-Z0-9]+", "_", payee)[:40] or "unknown"
            wiki_path = WIKI_DIR / f"finance_tx_{entry_id}.json"
            if wiki_path.exists():
                continue
            dispute = self._build_dispute_draft(tx)
            entry = {
                "type": "finance_transaction",
                "source": "moneytor",
                "provenance": self._provenance(),
                "payee": payee,
                "amount": amount,
                "date": tx.get("date"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "dispute_drafts": dispute,
            }
            wiki_path.write_text(json.dumps(entry, indent=2, ensure_ascii=False), encoding="utf-8")
            new_unknown.append(entry)
        return {"synced": len(txs), "new_wiki_entries": len(new_unknown), "entries": new_unknown}

    def _build_dispute_draft(self, tx: dict[str, Any]) -> dict[str, str]:
        payee = tx.get("payee", "")
        amount = tx.get("amount", "")
        date = tx.get("date", "")
        he = DISPUTE_DIR / "dispute_he.txt"
        en = DISPUTE_DIR / "dispute_en.txt"
        he_tpl = he.read_text(encoding="utf-8") if he.exists() else ""
        en_tpl = en.read_text(encoding="utf-8") if en.exists() else ""
        ctx = {"payee": payee, "amount": amount, "date": date}
        return {
            "he": he_tpl.format(**ctx) if he_tpl else "",
            "en": en_tpl.format(**ctx) if en_tpl else "",
        }


def main() -> None:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--since-days", type=int, default=30)
    args = p.parse_args()
    result = FinanceTracker().sync(since_days=args.since_days)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
