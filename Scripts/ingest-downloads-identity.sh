#!/usr/bin/env bash
# Copy safe identity-audit exports from ~/Downloads into identity/_inbox/
# Usage:
#   ingest-downloads-identity.sh [--dry-run]
#   ingest-downloads-identity.sh [--dry-run] --include-apple-license
#
# Allowlisted: Tailscale/GitHub exports, banking audit MD, optional apple.md,
#              redacted Meta/account-center *summary* markdown only (not session HTML).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INBOX="${REPO_ROOT}/Agent_Context/Knowledge_Base/identity/_inbox"
DOWNLOADS="${HOME}/Downloads"
DRY_RUN=0
INCLUDE_APPLE_LICENSE=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --include-apple-license) INCLUDE_APPLE_LICENSE=1 ;;
    -h|--help)
      echo "Usage: $(basename "$0") [--dry-run] [--include-apple-license]"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

# Extensions and patterns to NEVER copy
BLOCKED_EXT=(
  cer mobileconfig dmg vsix mp3 mp4 m4a opus vcf pem key pdf
)
BLOCKED_NAME_PATTERNS=(
  'recovery'
  'huggingface-recovery-codes'
  'secret'
  'credential'
  'id_rsa'
)

# Prefix allowlist (basename starts with)
ALLOWLIST=(
  'unified-system-core.org.github-devices'
  'export-Unified-system-Core'
  'export-igor-goncharenko'
  'export_2026-01-15'
  'The Professional Portfolio of Igor Goncharenko'
  'Israel Banking and Credit Transaction Leakage Audit'
)

# Exact or suffix-safe markdown summaries (NOT session HTML dumps)
SUMMARY_MD_PATTERNS=(
  'meta-accounts-summary'
  'account-center-summary'
  'accounts-center-summary'
  'account_center_summary'
)

# Explicit deny even if matched
DENYLIST=(
  'Центр аккаунтов.html'
  'huggingface-recovery-codes.txt'
)

# HTML never ingested except explicit future allowlist (empty = deny all .html)
HTML_ALLOWLIST=()

is_blocked() {
  local base="$1"
  local ext="${base##*.}"
  local lower_base
  lower_base="$(echo "$base" | tr '[:upper:]' '[:lower:]')"

  for d in "${DENYLIST[@]}"; do
    [[ "$base" == "$d" ]] && return 0
  done

  for e in "${BLOCKED_EXT[@]}"; do
    [[ "$ext" == "$e" ]] && return 0
  done

  for pat in "${BLOCKED_NAME_PATTERNS[@]}"; do
    [[ "$lower_base" == *"$pat"* ]] && return 0
  done

  # Block Meta / account center session HTML by keyword
  if [[ "$ext" == "html" || "$ext" == "htm" ]]; then
    if [[ "$lower_base" == *"аккаунт"* || "$lower_base" == *account*center* ]]; then
      local allowed=0
      if ((${#HTML_ALLOWLIST[@]})); then
        for h in "${HTML_ALLOWLIST[@]}"; do
          [[ "$base" == "$h" ]] && allowed=1
        done
      fi
      [[ $allowed -eq 0 ]] && return 0
    fi
    # Deny all other HTML unless explicitly allowlisted
    local html_ok=0
    if ((${#HTML_ALLOWLIST[@]})); then
      for h in "${HTML_ALLOWLIST[@]}"; do
        [[ "$base" == "$h" ]] && html_ok=1
      done
    fi
    [[ $html_ok -eq 0 ]] && return 0
  fi

  return 1
}

allowed_prefix() {
  local base="$1"
  for prefix in "${ALLOWLIST[@]}"; do
    [[ "$base" == "$prefix"* ]] && return 0
  done
  return 1
}

allowed_summary_md() {
  local base="$1"
  local lower_base
  lower_base="$(echo "$base" | tr '[:upper:]' '[:lower:]')"
  [[ "${base##*.}" == "md" ]] || return 1
  for pat in "${SUMMARY_MD_PATTERNS[@]}"; do
    [[ "$lower_base" == *"$pat"* ]] && return 0
  done
  return 1
}

copy_one() {
  local src="$1"
  local base
  base="$(basename "$src")"

  if is_blocked "$base"; then
    echo "SKIP (blocked): $base"
    return
  fi

  if ! allowed_prefix "$base" && ! allowed_summary_md "$base"; then
    echo "SKIP (not allowlisted): $base"
    return
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "DRY-RUN copy: $src -> $INBOX/$base"
  else
    mkdir -p "$INBOX"
    cp -p "$src" "$INBOX/$base"
    echo "COPIED: $base"
  fi
}

mkdir -p "$INBOX"

echo "=== Identity ingest (dry_run=$DRY_RUN, apple_license=$INCLUDE_APPLE_LICENSE) ==="
echo "Source: $DOWNLOADS"
echo "Target: $INBOX"
echo ""

shopt -s nullglob
for prefix in "${ALLOWLIST[@]}"; do
  for f in "${DOWNLOADS}/${prefix}"*; do
    [[ -f "$f" ]] || continue
    copy_one "$f"
  done
done

for pat in "${SUMMARY_MD_PATTERNS[@]}"; do
  for f in "$DOWNLOADS"/*"${pat}"*.md; do
    [[ -f "$f" ]] || continue
    copy_one "$f"
  done
done

if [[ $INCLUDE_APPLE_LICENSE -eq 1 && -f "$DOWNLOADS/apple.md" ]]; then
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "DRY-RUN copy (apple license text): $DOWNLOADS/apple.md"
  else
    cp -p "$DOWNLOADS/apple.md" "$INBOX/apple.md"
    echo "COPIED: apple.md (Tailscale license — not Apple ID roster)"
  fi
else
  if [[ -f "$DOWNLOADS/apple.md" ]]; then
    echo "SKIP (optional): apple.md — pass --include-apple-license to copy"
  fi
fi

if [[ -f "$DOWNLOADS/Центр аккаунтов.html" ]]; then
  echo "SKIP (blocked session dump): Центр аккаунтов.html — use typed meta-accounts-summary.md instead"
fi

echo ""
echo "Done. Review SENSITIVE_DO_NOT_IMPORT.md before merging into registry.yaml."
