---
name: uv-toolchain
description: UV-exclusive dependency management - NEVER use pip; uv is faster, deterministic, project-isolated
parent: global1sim-development
mandatory: true
replaces: pip
---

# UV Toolchain (Never Pip!)

**AGENTIC RULE**: NEVER use pip. Always use uv.

## Quick Reference (LLM: Memorize This)

```bash
# Add dependency
uv add package-name

# Add dev dependency
uv add --dev pytest ruff mypy

# Sync dependencies
uv sync

# Run command in uv environment
uv run pytest
uv run python script.py
uv run ruff check
uv run mypy src/

# NEVER use these:
# pip install (FORBIDDEN)
# pip freeze (use uv.lock instead)
```

## Why UV? (LLM: Explain This)

**Benefits**:
1. **Faster** than pip (Rust-based)
2. **Deterministic** (uv.lock guarantees reproducibility)
3. **Project-isolated** (no global pollution)
4. **Better resolution** (handles conflicts better)

**Book alignment**: Fast feedback (uv is faster = quicker iterations)

## Decision Tree

```yaml
need_to:
  add_package: uv add package-name
  add_dev_tool: uv add --dev tool-name
  run_tests: uv run pytest
  run_script: uv run python script.py
  check_types: uv run mypy src/
  format_code: uv run ruff format
  
never:
  pip_install: FORBIDDEN (use uv add)
  pip_freeze: FORBIDDEN (uv.lock auto-generated)
```

## Integration

- Mandatory for: ALL Global1SIM work
- Skills: `iterative-development` (fast tooling = fast feedback)
