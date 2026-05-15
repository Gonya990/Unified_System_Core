#!/usr/bin/env bash
# Collect local evidence for a one-button repository revision to PO workflow.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUN_ID="${RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}"
OUT_DIR="${PO_WORKFLOW_OUT:-$ROOT_DIR/Reports/po_workflow/$RUN_ID}"

WITH_NPM_AUDIT=0
WITH_PIP_AUDIT=0
WITH_DRIVE_SYNC=0
WITH_BEADS_CREATE=0

usage() {
  cat <<'USAGE'
Usage: bash Scripts/Orchestration/one_button_po.sh [options]

Options:
  --with-npm-audit    Run npm audit for tracked package-lock.json directories.
  --with-pip-audit    Run pip-audit for tracked requirements files when available.
  --drive-sync        Run $GOOGLE_DRIVE_SYNC_CMD after local evidence is generated.
  --create-beads      Create a Beads task if bd is available.
  -h, --help          Show this help.

The default mode is local-only and has no external side effects.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-npm-audit)
      WITH_NPM_AUDIT=1
      shift
      ;;
    --with-pip-audit)
      WITH_PIP_AUDIT=1
      shift
      ;;
    --drive-sync)
      WITH_DRIVE_SYNC=1
      shift
      ;;
    --create-beads)
      WITH_BEADS_CREATE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
  esac
done

mkdir -p "$OUT_DIR/scanner-output" "$OUT_DIR/evidence"

run_capture() {
  local name="$1"
  shift
  {
    echo "+ $*"
    "$@"
  } > "$OUT_DIR/$name" 2>&1 || {
    local code=$?
    echo "Command failed with exit code $code: $*" >> "$OUT_DIR/$name"
    return 0
  }
}

command_path() {
  if command -v "$1" >/dev/null 2>&1; then
    command -v "$1"
  else
    echo "missing"
  fi
}

cd "$ROOT_DIR"

{
  echo "run_id=$RUN_ID"
  echo "root=$ROOT_DIR"
  echo "created_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_sha=$(git rev-parse HEAD 2>/dev/null || true)"
  echo "branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
} > "$OUT_DIR/metadata.env"

{
  echo "git=$(command_path git)"
  echo "npm=$(command_path npm)"
  echo "python3=$(command_path python3)"
  echo "pip-audit=$(command_path pip-audit)"
  echo "gitleaks=$(command_path gitleaks)"
  echo "trufflehog=$(command_path trufflehog)"
  echo "firebase=$(command_path firebase)"
  echo "bd=$(command_path bd)"
  echo "rg=$(command_path rg)"
} > "$OUT_DIR/tool-availability.txt"

run_capture "git-status.txt" git status --short --branch
run_capture "git-log.txt" git log --oneline -20
run_capture "submodules.txt" git submodule status --recursive

if command -v rg >/dev/null 2>&1; then
  git ls-files \
    | rg -i '(^|/)\.next/|(^|/)\.env|credentials|service-account|secret|token|\.log$|debug|configmap|firebase-debug' \
    > "$OUT_DIR/tracked-risk-named-files.txt" || true
else
  echo "rg missing; skipped tracked risk file scan" > "$OUT_DIR/tracked-risk-named-files.txt"
fi

if [[ "$WITH_NPM_AUDIT" -eq 1 ]]; then
  if ! command -v npm >/dev/null 2>&1; then
    echo "npm is not available" > "$OUT_DIR/scanner-output/npm-audit-summary.txt"
  else
    : > "$OUT_DIR/scanner-output/npm-audit-summary.txt"
    while IFS= read -r lockfile; do
      dir="${lockfile%/package-lock.json}"
      [[ "$dir" == "$lockfile" ]] && dir="."
      safe_name="${dir//\//_}"
      echo "=== $dir ===" >> "$OUT_DIR/scanner-output/npm-audit-summary.txt"
      (
        cd "$ROOT_DIR/$dir"
        npm audit --omit=dev --json > "$OUT_DIR/scanner-output/npm-audit-$safe_name.json"
      ) || true
      python3 - "$dir" "$OUT_DIR/scanner-output/npm-audit-$safe_name.json" >> "$OUT_DIR/scanner-output/npm-audit-summary.txt" <<'PY' || true
import json
import sys

name, path = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(path, encoding="utf-8"))
except Exception as exc:
    print(f"{name}: unable to parse npm audit output: {exc}")
    raise SystemExit(0)

vulns = data.get("metadata", {}).get("vulnerabilities", {})
print(f"{name}: {vulns}")
PY
    done < <(git ls-files | rg '(^|/)package-lock\.json$' || true)
  fi
fi

if [[ "$WITH_PIP_AUDIT" -eq 1 ]]; then
  if python3 -m pip_audit --help >/dev/null 2>&1; then
    : > "$OUT_DIR/scanner-output/pip-audit-summary.txt"
    while IFS= read -r reqfile; do
      safe_name="${reqfile//\//_}"
      echo "=== $reqfile ===" >> "$OUT_DIR/scanner-output/pip-audit-summary.txt"
      python3 -m pip_audit \
        -r "$reqfile" \
        --no-deps \
        --disable-pip \
        --format json \
        --progress-spinner off \
        > "$OUT_DIR/scanner-output/pip-audit-$safe_name.json" \
        2> "$OUT_DIR/scanner-output/pip-audit-$safe_name.err" || true
      python3 - "$reqfile" "$OUT_DIR/scanner-output/pip-audit-$safe_name.json" "$OUT_DIR/scanner-output/pip-audit-$safe_name.err" >> "$OUT_DIR/scanner-output/pip-audit-summary.txt" <<'PY' || true
import json
import sys

name, out_path, err_path = sys.argv[1:4]
text = open(out_path, encoding="utf-8", errors="ignore").read().strip()
if text.startswith("{"):
    data = json.loads(text)
    count = 0
    packages = set()
    for dep in data.get("dependencies", []):
        vulns = dep.get("vulns") or []
        count += len(vulns)
        if vulns:
            packages.add(dep.get("name"))
    print(f"{name}: vulnerable_packages={len(packages)}, vulnerabilities={count}")
else:
    err = open(err_path, encoding="utf-8", errors="ignore").read().strip().splitlines()
    print(f"{name}: unsupported or failed; {err[0] if err else 'no details'}")
PY
    done < <(git ls-files | rg '(^|/)requirements.*\.txt$' || true)
  else
    echo "python3 -m pip_audit is not available" > "$OUT_DIR/scanner-output/pip-audit-summary.txt"
  fi
fi

cat > "$OUT_DIR/README.md" <<EOF
# One-Button PO Evidence Run

Run ID: \`$RUN_ID\`

This folder contains local evidence collected by \`Scripts/Orchestration/one_button_po.sh\`.

Core files:

- \`metadata.env\` - run metadata.
- \`tool-availability.txt\` - available local tools.
- \`git-status.txt\` - repository status.
- \`git-log.txt\` - recent commits.
- \`submodules.txt\` - submodule revisions.
- \`tracked-risk-named-files.txt\` - tracked paths whose names suggest credentials, debug files, tokens, ConfigMaps, or generated Next.js output.
- \`scanner-output/\` - optional npm/pip audit outputs.

External actions are disabled by default. Use \`--drive-sync\` or \`--create-beads\` only after the required environment variables and credentials are configured.
EOF

if [[ "$WITH_DRIVE_SYNC" -eq 1 ]]; then
  if [[ -z "${GOOGLE_DRIVE_SYNC_CMD:-}" ]]; then
    echo "GOOGLE_DRIVE_SYNC_CMD is required for --drive-sync" >&2
    exit 3
  fi
  echo "Running Google Drive sync command..."
  bash -lc "$GOOGLE_DRIVE_SYNC_CMD"
fi

if [[ "$WITH_BEADS_CREATE" -eq 1 ]]; then
  if ! command -v bd >/dev/null 2>&1; then
    echo "bd is required for --create-beads" >&2
    exit 4
  fi
  bd create "Review PO evidence run $RUN_ID" --type task --priority 2 --description "Evidence folder: $OUT_DIR"
fi

echo "PO evidence run created: $OUT_DIR"
