"""
Conscience Module
=================
Acts as the moral compass and rule enforcer for the Unified System.
Reads constraints from NOTEBOOK.md and enforces them on system actions.
"""

import re
from pathlib import Path


class Conscience:
    def __init__(self, notebook_path: str = "NOTEBOOK.md"):
        self.notebook_path = Path(notebook_path).resolve()
        self.rules = []
        self.load_rules()

    def load_rules(self):
        """Parses NOTEBOOK.md for 'Rule:' or 'Action:' directives."""
        if not self.notebook_path.exists():
            print(f"⚠️ Conscience: Notebook not found at {self.notebook_path}")
            return

        with open(self.notebook_path, encoding="utf-8") as f:
            content = f.read()

        # Simple parsing logic
        # Looks for lines like: "**Rule:** Do NOT do X"
        rule_pattern = re.compile(r"\*\*(Rule|Action):\*\*\s*(.+)", re.IGNORECASE)

        self.rules = []
        for line in content.splitlines():
            match = rule_pattern.search(line)
            if match:
                self.rules.append({"type": match.group(1).upper(), "text": match.group(2).strip()})

    def check_action(self, action_description: str) -> bool:
        """
        Consults the rules to see if an action is permissible.
        Returns True if allowed, False if blocked.
        """
        # Reload rules dynamically (conscience is always learning)
        self.load_rules()

        print(f"⚖️ Conscience Context: Checking action '{action_description}'")

        for rule in self.rules:
            # Very basic keyword matching for now
            # Real implementation would use LLM or strict keyword maps
            if "deploy" in action_description.lower() and "do not deploy" in rule["text"].lower():
                print(f"⛔ BLOCKED by Rule: {rule['text']}")
                return False

            if "implement" in action_description.lower() and "until spec is approved" in rule["text"].lower():
                print(f"⛔ BLOCKED by Rule: {rule['text']}")
                return False

        return True

    def state_rules(self):
        """Prints current laws."""
        print("\n📜 The Laws of This Session:")
        for r in self.rules:
            print(f"  • [{r['type']}] {r['text']}")
        print()
