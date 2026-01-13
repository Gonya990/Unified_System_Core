import json
import re
import subprocess
import sys
from datetime import datetime

TRAILER_PATTERN = re.compile(r"^(?P<key>[a-zA-Z0-9-]+):\s*(?P<value>.+)$")


def get_last_commit_trailers():
    """Extracts trailers from the last commit."""
    try:
        # Get the full commit message
        result = subprocess.run(["git", "log", "-1", "--pretty=format:%B"], capture_output=True, text=True, check=True)
        message = result.stdout.strip()
        lines = message.split("\n")

        trailers = {}
        # Simple trailer parsing (looks at last block of lines)
        for line in reversed(lines):
            line = line.strip()
            if not line:
                break

            match = TRAILER_PATTERN.match(line)
            if match:
                trailers[match.group("key")] = match.group("value")

        return trailers, message
    except Exception as e:
        print(f"Error extracting trailers: {e}")
        return {}, ""


def distill_claims(trailers, message):
    """Distills REP claims from trailers."""
    claims = []

    # 1. Task Linkage Claim
    if "Task-Id" in trailers:
        claims.append({"type": "Linkage", "task_id": trailers["Task-Id"], "timestamp": datetime.utcnow().isoformat()})

    # 2. Sensitivity Claim (REP)
    if "REP-Sensitivity" in trailers:
        sensitivity_text = trailers["REP-Sensitivity"]
        # Simple heuristic parser for IF/THEN (can be upgraded to LLM later)
        if_part = ""
        then_part = ""

        if "IF " in sensitivity_text and "THEN " in sensitivity_text:
            parts = sensitivity_text.split("THEN ")
            if_part = parts[0].replace("IF ", "").strip()
            then_part = parts[1].strip()

        claims.append(
            {
                "type": "Sensitivity",
                "trigger": if_part,
                "impact": then_part,
                "raw": sensitivity_text,
                "variables": trailers.get("REP-Variables", "unknown").split(","),
                "confidence": 1.0,  # Human authored
            }
        )

    return claims


def save_claims(claims, commit_hash):
    """Saves distilled claims to the rep/claims directory."""
    if not claims:
        print("No claims found.")
        return

    filename = f"rep/claims/{commit_hash}.json"
    try:
        with open(filename, "w") as f:
            json.dump(claims, f, indent=2)
        print(f"Saved {len(claims)} claims to {filename}")
    except Exception as e:
        print(f"Error saving claims: {e}")


def main():
    try:
        # Get commit hash
        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        commit_hash = result.stdout.strip()

        trailers, message = get_last_commit_trailers()
        claims = distill_claims(trailers, message)
        save_claims(claims, commit_hash)

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
