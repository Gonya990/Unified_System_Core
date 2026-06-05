#!/usr/bin/env bash
set -euo pipefail

SRC="/Users/igorgoncharenko/unified-core-staging"
DST="/Users/igorgoncharenko/Documents/Unified_System_Core"

if [[ ! -d "$SRC" ]]; then
  echo "Missing staging: $SRC" >&2
  exit 1
fi

if [[ ! -w "$DST" ]] 2>/dev/null; then
  echo "Cannot write to $DST — grant Full Disk Access or run manually:" >&2
  echo "  rsync -av --exclude .venv $SRC/ $DST/" >&2
  exit 1
fi

echo "Syncing guardrails slice into monorepo..."
rsync -av --delete \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '.git' \
  "$SRC/config/" "$DST/config/" 2>/dev/null || mkdir -p "$DST/config" && rsync -av "$SRC/config/" "$DST/config/"

for dir in services docs lib scripts infra templates data .cursor; do
  mkdir -p "$DST/$dir"
  rsync -av "$SRC/$dir/" "$DST/$dir/" 2>/dev/null || true
done

[[ -f "$SRC/SYSTEM_MAP.md" ]] && cp "$SRC/SYSTEM_MAP.md" "$DST/SYSTEM_MAP.md"
echo "Done. Review git diff in $DST"
