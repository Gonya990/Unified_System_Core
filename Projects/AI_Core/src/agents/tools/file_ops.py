"""
File Operations Tool for AI Agent

Provides safe file system operations for the agent.
"""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class FileOpsTool:
    """File system operations tool"""

    @staticmethod
    def get_definition() -> dict[str, Any]:
        """Get OpenAI function definition for file_read"""
        return {
            "name": "file_read",
            "description": "Read contents of a file. Returns file content with size info.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to file to read"},
                    "max_chars": {
                        "type": "integer",
                        "description": "Maximum characters to return (default: 5000)",
                        "default": 5000,
                    },
                },
                "required": ["path"],
            },
        }

    @staticmethod
    async def handler(path: str, max_chars: int = 5000) -> str:
        """
        Read file contents.

        Args:
            path: Absolute path to file
            max_chars: Maximum characters to return

        Returns:
            File content with metadata
        """
        try:
            file_path = Path(path).expanduser().resolve()

            if not file_path.exists():
                return f"❌ Error: File not found: {path}"

            if not file_path.is_file():
                return f"❌ Error: Path is not a file: {path}"

            # Read file
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            total_size = len(content)

            # Truncate if needed
            if total_size > max_chars:
                content = content[:max_chars]
                truncated_msg = f"\n\n... (truncated {total_size - max_chars} characters)"
            else:
                truncated_msg = ""

            return f"""📄 **File:** {file_path.name}
📍 **Path:** {path}
📏 **Size:** {total_size} characters

**Content:**
```
{content}{truncated_msg}
```"""

        except UnicodeDecodeError:
            return f"❌ Error: File is not text (binary file): {path}"
        except PermissionError:
            return f"❌ Error: Permission denied: {path}"
        except Exception as e:
            logger.error(f"Error reading file {path}: {e}", exc_info=True)
            return f"❌ Error reading file: {str(e)}"


class FileListTool:
    """Directory listing tool"""

    @staticmethod
    def get_definition() -> dict[str, Any]:
        """Get OpenAI function definition for file_list"""
        return {
            "name": "file_list",
            "description": "List files and directories in a given path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to directory"},
                    "pattern": {
                        "type": "string",
                        "description": "Optional glob pattern (e.g., '*.py')",
                        "default": "*",
                    },
                },
                "required": ["path"],
            },
        }

    @staticmethod
    async def handler(path: str, pattern: str = "*") -> str:
        """
        List directory contents.

        Args:
            path: Absolute path to directory
            pattern: Glob pattern for filtering

        Returns:
            Formatted directory listing
        """
        try:
            dir_path = Path(path).expanduser().resolve()

            if not dir_path.exists():
                return f"❌ Error: Directory not found: {path}"

            if not dir_path.is_dir():
                return f"❌ Error: Path is not a directory: {path}"

            # List files
            items = sorted(dir_path.glob(pattern))

            if not items:
                return f"📁 **Directory:** {path}\n\n(Empty or no matches for pattern '{pattern}')"

            files = [item for item in items if item.is_file()]
            dirs = [item for item in items if item.is_dir()]

            result = f"📁 **Directory:** {path}\n\n"

            if dirs:
                result += "**Directories:**\n"
                for d in dirs[:50]:  # Limit to 50
                    result += f"  📁 {d.name}/\n"
                if len(dirs) > 50:
                    result += f"  ... and {len(dirs) - 50} more directories\n"
                result += "\n"

            if files:
                result += "**Files:**\n"
                for f in files[:50]:  # Limit to 50
                    size = f.stat().st_size
                    size_str = f"{size:,} bytes" if size < 1024 else f"{size / 1024:.1f} KB"
                    result += f"  📄 {f.name} ({size_str})\n"
                if len(files) > 50:
                    result += f"  ... and {len(files) - 50} more files\n"

            return result

        except PermissionError:
            return f"❌ Error: Permission denied: {path}"
        except Exception as e:
            logger.error(f"Error listing directory {path}: {e}", exc_info=True)
            return f"❌ Error listing directory: {str(e)}"
