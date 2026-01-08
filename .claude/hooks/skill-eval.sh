#!/bin/bash
# Skill Evaluation Hook for UserPromptSubmit
# Analyzes user prompts and suggests relevant skills
# Adapted from ChrisWiles/claude-code-showcase

# Read the prompt from stdin
input=$(cat)

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    # If Node.js is not available, pass through without evaluation
    exit 0
fi

# Pass to the JavaScript evaluator
echo "$input" | node "$(dirname "$0")/skill-eval.js"

# Always exit 0 to allow the prompt through
# The JS script outputs feedback but doesn't block
exit 0
