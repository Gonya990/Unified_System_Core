from __future__ import annotations

import json
import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any


@dataclass
class PolicyDecision:
    allowed: bool
    action: str  # allow | deny | require_yubikey
    risk_score: float
    rule_id: str | None
    domain: str | None
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "action": self.action,
            "risk_score": self.risk_score,
            "rule_id": self.rule_id,
            "domain": self.domain,
            "reasons": self.reasons,
        }


class PolicyEngine:
    def __init__(self, policy_path: Path | None = None) -> None:
        root = Path(__file__).resolve().parents[3]
        self.policy_path = policy_path or (root / "config" / "policy.json")
        self._policy = self._load()

    def _load(self) -> dict[str, Any]:
        with open(self.policy_path, encoding="utf-8") as f:
            return json.load(f)

    def reload(self) -> None:
        self._policy = self._load()

    def evaluate(
        self,
        *,
        command: str | None = None,
        path: str | None = None,
        intent: str | None = None,
    ) -> PolicyDecision:
        cmd = (command or "").strip()
        p = (path or "").strip()
        reasons: list[str] = []

        for allowed in self._policy.get("allowlist_commands", []):
            if cmd == allowed or cmd.startswith(allowed + " "):
                return PolicyDecision(
                    allowed=True,
                    action="allow",
                    risk_score=0.0,
                    rule_id="allowlist",
                    domain=None,
                    reasons=["Explicit allowlist match"],
                )

        best_score = 0.0
        best_rule: dict[str, Any] | None = None

        for rule in self._policy.get("rules", []):
            if not self._rule_matches(rule, command=cmd, path=p):
                continue
            score = float(rule.get("risk_score", 0.5))
            if score >= best_score:
                best_score = score
                best_rule = rule

        if intent and any(
            w in intent.lower()
            for w in ("delete", "destroy", "transfer", "payment", "secret", "sudo", "root")
        ):
            best_score = max(best_score, 0.35)
            reasons.append(f"Intent heuristic: {intent[:120]}")

        if not best_rule:
            default = self._policy.get("default_action", "allow")
            if default == "deny":
                return PolicyDecision(
                    allowed=False,
                    action="deny",
                    risk_score=0.5,
                    rule_id=None,
                    domain=None,
                    reasons=["No rule matched — default_action deny"],
                )
            return PolicyDecision(
                allowed=True,
                action="allow",
                risk_score=0.1,
                rule_id=None,
                domain=None,
                reasons=["No rule matched — default allow"],
            )

        action = best_rule.get("action", "deny")
        domain = best_rule.get("domain")
        rule_id = best_rule.get("id")
        reasons.append(f"Matched rule {rule_id} ({domain})")

        if action == "deny":
            return PolicyDecision(
                allowed=False,
                action="deny",
                risk_score=best_score,
                rule_id=rule_id,
                domain=domain,
                reasons=reasons,
            )
        if action == "require_yubikey":
            return PolicyDecision(
                allowed=False,
                action="require_yubikey",
                risk_score=best_score,
                rule_id=rule_id,
                domain=domain,
                reasons=reasons + ["YubiKey touch required"],
            )
        return PolicyDecision(
            allowed=True,
            action="allow",
            risk_score=best_score,
            rule_id=rule_id,
            domain=domain,
            reasons=reasons,
        )

    def _rule_matches(self, rule: dict[str, Any], *, command: str, path: str) -> bool:
        match = rule.get("match", {})
        mtype = match.get("type")
        pattern = match.get("pattern", "")
        field = match.get("field", "command")
        value = command if field == "command" else path
        if not value:
            return False
        if mtype == "regex":
            return bool(re.search(pattern, value, re.IGNORECASE))
        if mtype == "path_prefix":
            expanded = pattern.replace("~", str(Path.home()))
            return value.startswith(expanded) or value.startswith(pattern)
        if mtype == "glob":
            return fnmatch(value, pattern)
        return False

    def get_risk_score(
        self, *, command: str | None = None, path: str | None = None, intent: str | None = None
    ) -> dict[str, Any]:
        d = self.evaluate(command=command, path=path, intent=intent)
        blocked = d.action == "deny" or d.action == "require_yubikey"
        return {
            "score": d.risk_score,
            "blocked": blocked,
            "action": d.action,
            "reasons": d.reasons,
            "rule_id": d.rule_id,
            "domain": d.domain,
        }
