#!/usr/bin/env bash
# Wrapper for ubs (Ultimate Bug Scanner)
UBS_BIN="/Users/macbook/Documents/Unified_System/External_Tools/Stack/ubs"

if [ ! -x "$UBS_BIN" ]; then
    echo "Error: ubs binary not found or not executable at $UBS_BIN"
    exit 1
fi

"$UBS_BIN" "$@"
