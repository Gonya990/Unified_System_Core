#!/bin/bash
# Ultimate Bug Scanner - Claude Code Hook
# Runs on every file save for UBS-supported languages

if [[ "$FILE_PATH" =~ \.(js|jsx|ts|tsx|mjs|cjs|py|pyw|pyi|c|cc|cpp|cxx|h|hh|hpp|hxx|rs|go|java|rb)$ ]]; then
  # Dynamic reminder based on language-preferences.json
  # Defaulting to Kosta's preference for this host
  echo "🔬 Running bug scanner... REMINDER: Follow Per-User Language Protocol (Check language-preferences.json)"
  
  if ! command -v ubs >/dev/null 2>&1; then
    echo "⚠️  'ubs' not found in PATH; install it before using this hook." >&2
    exit 0
  fi
  ubs "${PROJECT_DIR}" --ci 2>&1 | head -50
fi
