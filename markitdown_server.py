import os

from markitdown import MarkItDown
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("MarkItDown")
markitdown = MarkItDown()


@mcp.tool()
def convert_to_markdown(file_path: str) -> str:
    """Convert a file (PDF, DOCX, XLSX, etc.) to Markdown."""
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    try:
        result = markitdown.convert(file_path)
        return result.text_content
    except Exception as e:
        return f"Error converting file: {str(e)}"


if __name__ == "__main__":
    mcp.run()
