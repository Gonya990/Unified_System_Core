"""
Notion Client
Integration with Notion API for creating notes and tasks.
"""
import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class NotionClient:
    """Client for Notion API."""

    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.client = None

        if self.api_key:
            try:
                from notion_client import AsyncClient
                self.client = AsyncClient(auth=self.api_key)
                logger.info("Notion client initialized")
            except ImportError:
                logger.error("notion-client library not installed")
            except Exception as e:
                logger.error(f"Failed to initialize Notion client: {e}")
        else:
            logger.warning("NOTION_API_KEY not set")

    async def create_page(self, title: str, content: str = "", tags: List[str] = None) -> Optional[str]:
        """Create a new page in the database."""
        if not self.client or not self.database_id:
            logger.error("Notion client not configured (missing key or DB ID)")
            return None

        try:
            properties = {
                "Name": {"title": [{"text": {"content": title}}]},
            }

            if tags:
                properties["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}

            children = []
            if content:
                # Split content by newlines for basic formatting
                for line in content.split('\n'):
                    if line.strip():
                        children.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": line}}]
                            }
                        })

            response = await self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )

            return response.get("url")

        except Exception as e:
            logger.error(f"Failed to create Notion page: {e}")
            return None

    async def search_pages(self, query: str) -> List[Dict]:
        """Search for pages."""
        if not self.client:
            return []

        try:
            response = await self.client.search(query=query)
            results = []
            for page in response.get("results", []):
                if page["object"] == "page":
                    title = "Untitled"
                    # Try to find title in properties
                    props = page.get("properties", {})
                    for key, val in props.items():
                        if val["id"] == "title":
                             if val["title"]:
                                 title = val["title"][0]["text"]["content"]
                                 break
                    results.append({"title": title, "url": page["url"]})
            return results
        except Exception as e:
            logger.error(f"Notion search failed: {e}")
            return []
