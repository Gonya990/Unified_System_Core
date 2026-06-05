#!/usr/bin/env bash
# Import NotebookLM exports into Knowledge_Base staging (_inbox → curated manually).
# Usage:
#   ./scripts/import-notebooklm.sh [--dry-run]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="${REPO_ROOT}/Agent_Context/Knowledge_Base/notebooklm"
INBOX="${BASE}/_inbox"
CURATED="${BASE}/curated"
DESKTOP_SRC="${HOME}/Desktop/NotebookLM"
DOWNLOADS="${HOME}/Downloads"
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help)
      echo "Usage: $(basename "$0") [--dry-run]"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$INBOX" "$CURATED"

stamp() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

add_frontmatter() {
  local dest="$1"
  local src_path="$2"
  local base
  base="$(basename "$dest")"
  local title="${base%.*}"
  title="${title//_/ }"

  if [[ -f "$dest" ]] && head -n1 "$dest" | grep -q '^---$'; then
    return 0
  fi

  local tmp
  tmp="$(mktemp)"
  {
    echo "---"
    echo "source: notebooklm"
    echo "imported_at: $(stamp)"
    echo "original_path: ${src_path}"
    echo "title: ${title}"
    echo "status: inbox"
    echo "---"
    echo ""
    if [[ -f "$dest" ]]; then
      cat "$dest"
    fi
  } >"$tmp"
  if [[ "$DRY_RUN" -eq 0 ]]; then
    mv "$tmp" "$dest"
  else
    rm -f "$tmp"
  fi
}

copy_one() {
  local src="$1"
  [[ -e "$src" ]] || return 0
  local base dest
  base="$(basename "$src")"
  dest="${INBOX}/${base}"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] would copy: $src -> $dest"
    return 0
  fi

  if [[ -d "$src" ]]; then
    mkdir -p "$dest"
    find "$src" -type f \( -name '*.md' -o -name '*.txt' -o -name '*.pdf' \) -print0 2>/dev/null | while IFS= read -r -d '' f; do
      rel="${f#"$src"/}"
      mkdir -p "$(dirname "$dest/$rel")"
      cp -f "$f" "$dest/$rel"
      [[ "$rel" == *.md ]] && add_frontmatter "$dest/$rel" "$f"
    done
  else
    cp -f "$src" "$dest"
    [[ "$base" == *.md ]] && add_frontmatter "$dest" "$src"
  fi
  echo "imported: $base"
}

echo "NotebookLM import -> ${INBOX}"
[[ -d "$DESKTOP_SRC" ]] && copy_one "$DESKTOP_SRC"

shopt -s nullglob
for f in "$DOWNLOADS"/*[Nn]otebook[Ll][Mm]* "$DOWNLOADS"/*[Nn]otebook[Ll][Mm]*/*; do
  [[ -e "$f" ]] || continue
  copy_one "$f"
done
shopt -u nullglob

echo "Done. Review ${INBOX}, then promote files to ${CURATED} when ready."
