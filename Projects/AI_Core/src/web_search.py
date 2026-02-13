"""
Web Search Module for AI Telegram Bot.
Uses SerpApi (Google) if configured, else DuckDuckGo Search fallback.
"""

import asyncio
import logging
import os

logger = logging.getLogger(__name__)


class WebSearch:
    def __init__(self):
        self.available = False
        self.ddgs = None
        self.serp_api_key = os.getenv("SERPAPI_KEY")

        try:
            from ddgs import DDGS  # preferred (new package)

            self.ddgs = DDGS()
            self.available = True
        except ImportError:
            try:
                from duckduckgo_search import DDGS  # legacy fallback

                self.ddgs = DDGS()
                self.available = True
            except ImportError:
                logger.error("ddgs/duckduckgo-search not installed")
            except Exception as e:
                logger.error(f"Failed to init DDGS (legacy): {e}")
        except Exception as e:
            logger.error(f"Failed to init DDGS: {e}")

    async def search(self, query: str, max_results: int = 5) -> str:
        """
        Perform a web search using SerpApi (preferred) or DuckDuckGo (fallback).
        Executed in thread pool to avoid blocking async loop.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._do_search_sync, query, max_results)

    def _do_search_sync(self, query: str, max_results: int) -> str:
        # 1. Try SerpApi if Key exists
        if self.serp_api_key:
            try:
                from serpapi import GoogleSearch

                params = {
                    "engine": "google",
                    "q": query,
                    "api_key": self.serp_api_key,
                    "num": max_results,
                    "hl": "ru",  # Russian language preference
                    "gl": "ru",  # Location preference
                }
                search = GoogleSearch(params)
                results = search.get_dict()

                formatted_results = []

                # Knowledge Graph
                if "knowledge_graph" in results:
                    kg = results["knowledge_graph"]
                    title = kg.get("title", "")
                    desc = kg.get("description", "")
                    if title and desc:
                        formatted_results.append(f"🎓 **{title}**: {desc}\n")

                # Organic Results
                if "organic_results" in results:
                    for item in results["organic_results"][:max_results]:
                        title = item.get("title")
                        link = item.get("link")
                        snippet = item.get("snippet", "")
                        formatted_results.append(f"• [{title}]({link})\n  {snippet}")

                if formatted_results:
                    return "\n\n".join(formatted_results)

            except Exception as e:
                logger.error(f"SerpApi failed: {e}. Falling back to DuckDuckGo.")

        # 2. Fallback to DuckDuckGo
        if not self.available or not self.ddgs:
            return "❌ Search module unavailable."

        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            if not results:
                return f"🔍 По запросу '{query}' ничего не найдено."

            formatted_results = []
            for i, r in enumerate(results, 1):
                title = r.get("title", "No Title")
                link = r.get("href", "#")
                body = r.get("body", "")
                formatted_results.append(f"{i}. [{title}]({link})\n_{body}_")

            return "\n\n".join(formatted_results)

        except Exception as e:
            logger.error(f"DDG Search failed: {e}")
            return f"❌ Ошибка поиска: {e}"
