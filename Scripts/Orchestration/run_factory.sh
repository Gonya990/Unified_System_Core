#!/bin/bash
# Robust runner for Content Factory
# Ensures environment, paths and tokens are correctly set

# 1. Setup paths
# Detect OS and set root
if [[ "$OSTYPE" == "darwin"* ]]; then
    export ROOT_DIR="$HOME/Documents/Unified_System_Core"
else
    export ROOT_DIR="/home/gonya/Unified_System"
fi

export FACTORY_DIR="$ROOT_DIR/Projects/Content_Factory"
export VENV_PATH="$FACTORY_DIR/venv"
export PATH="$VENV_PATH/bin:/usr/local/bin:/usr/bin:/bin"

# 2. Master Token for TokenBroker
export AGENT_MAIL_TOKEN="c2bb2cf043ec2ae56a0dec69024e5129eb5cde36a22bddb93afcfa2e71e72afb"

# 3. Mode selector
MODE=$1
if [ -z "$MODE" ]; then
    MODE="--auto"
fi

# 4. Execute
cd "$FACTORY_DIR/src/pipeline"
echo "[$(date)] Starting Factory with mode: $MODE"
"$VENV_PATH/bin/python3" factory_scheduler.py $MODE
echo "[$(date)] Factory run completed."
