# Moneytor integration (read-only)

Provider: [Moneytor](https://moneytor.co.il/en/) — Israeli PFM with bank/pension/securities aggregation.

## Threat model

- Transaction data lives in Moneytor cloud (Azure). Unified Core stores **redacted summaries** in local `data/memory-wiki/`.
- Automation must **never** initiate payments via API.
- API keys in TokenBroker: `~/.config/unified-system/tokens.yaml` key `moneytor`.

## Integration paths (priority)

| Path | Env vars | Notes |
|------|----------|-------|
| A Official API | `MONEYTOR_API_URL`, `MONEYTOR_API_KEY` | Contact Moneytor support for developer access |
| B CSV export | `MONEYTOR_CSV_EXPORT=/path/to/export.csv` | Premium export → `finance_tracker` ingest |
| C Direct open banking | TBD | Only if A/B insufficient |
| D Manual assets | `config/finance_assets.yaml` | Copy from `finance_assets.yaml.example` |

## Behavior

1. Unknown transaction → `data/memory-wiki/finance_tx_*.json` (no push spam).
2. Budget review → Cursor MCP `memory_search` surfaces entries + `dispute_drafts` (he/en templates).
3. Recurring whitelist → `config/SOVEREIGN_MANIFEST.yaml` `domains.finance.whitelist_recurring`.

## Run

```bash
export MONEYTOR_CSV_EXPORT=~/Downloads/moneytor-export.csv
python3 -m finance_tracker.tracker --since-days 30
```

## Predictive alerts (phase 5)

OpenClaw cron job `finance_cashflow_check` compares:

- Moneytor balances (read-only)
- `finance_assets.yaml` manual liabilities
- Emits wiki entry if forecast cashflow &lt; threshold (no auto payments).
