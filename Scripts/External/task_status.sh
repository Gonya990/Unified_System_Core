#!/usr/bin/env bash
# Wrapper for bv (Beads Viewer) robot triage
BV_BIN="/Users/macbook/Documents/Unified_System/External_Tools/Stack/bv"

if [ ! -x "$BV_BIN" ]; then
    echo "Error: bv binary not found or not executable at $BV_BIN"
    exit 1
fi

"$BV_BIN" --robot-triage "$@"
