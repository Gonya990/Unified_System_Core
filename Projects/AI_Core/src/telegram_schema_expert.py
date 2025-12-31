import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class TelegramSchemaExpert:
    def __init__(self, schema_path: str = "data/telegram_schema.json"):
        root_dir = Path(__file__).parent
        self.schema_path = root_dir / schema_path
        self.data = {"constructors": [], "methods": []}
        self._load_schema()

    def _load_schema(self):
        try:
            if self.schema_path.exists():
                with open(self.schema_path, "r") as f:
                    self.data = json.load(f)
                logger.info(f"Loaded Telegram schema from {self.schema_path}")
            else:
                logger.warning(f"Telegram schema not found at {self.schema_path}")
        except Exception as e:
            logger.error(f"Failed to load Telegram schema: {e}")

    def lookup(self, query: str) -> str:
        """Find information about a constructor, method, or type."""
        query = query.strip().lower()
        
        # Search in constructors
        for c in self.data.get("constructors", []):
            if c["predicate"].lower() == query or str(c["id"]) == query:
                return self._format_obj(c, "Constructor")
        
        # Search in methods
        for m in self.data.get("methods", []):
            if m["method"].lower() == query or str(m["id"]) == query:
                return self._format_obj(m, "Method")

        # Search by type (list occurrences)
        by_type = []
        for c in self.data.get("constructors", []):
            if c["type"].lower() == query:
                by_type.append(f"• `{c['predicate']}`")
        if by_type:
            return f"Type `{query}` has constructors:\n" + "\n".join(by_type[:15]) + ("\n..." if len(by_type) > 15 else "")

        return f"🔍 Nothing found for `{query}` in TL Schema."

    def _format_obj(self, obj: Dict[str, Any], label: str) -> str:
        name = obj.get("predicate") or obj.get("method")
        params = obj.get("params", [])
        param_str = "\n".join([f"  - `{p['name']}`: `{p['type']}`" for p in params])
        
        res = f"📘 **{label}: {name}**\n"
        res += f"ID: `{obj['id']}`\n"
        res += f"Type: `{obj['type']}`\n"
        if params:
            res += f"Parameters:\n{param_str}\n"
        else:
            res += "Parameters: None\n"
        
        return res

    def get_stats(self) -> str:
        return f"📊 TL Schema: {len(self.data.get('constructors', []))} constructors, {len(self.data.get('methods', []))} methods."
