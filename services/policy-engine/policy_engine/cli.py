from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import PolicyEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified Core policy engine CLI")
    parser.add_argument("command", nargs="?", help="Shell command to evaluate")
    parser.add_argument("--path", help="File path context")
    parser.add_argument("--intent", help="Agent intent description")
    parser.add_argument(
        "--policy",
        type=Path,
        default=None,
        help="Path to policy.json",
    )
    sub = parser.add_subparsers(dest="sub")
    sub.add_parser("check", help="Evaluate command (default)")

    args = parser.parse_args()
    engine = PolicyEngine(args.policy)
    decision = engine.evaluate(command=args.command, path=args.path, intent=args.intent)
    print(json.dumps(decision.to_dict(), indent=2))
    return 0 if decision.allowed or decision.action == "require_yubikey" else 1


if __name__ == "__main__":
    sys.exit(main())
