"""
Web Search Module for AI Telegram Bot.
Uses DuckDuckGo Search to retrieve information/links from the web.
"""
import logging
import asyncio
from typing import List, Dict

logger = logging.getLogger(__name__)

class WebSearch:
    def __init__(self):
        try:
            from duckduckgo_search import DDGS
            self.ddgs = DDGS()
            self.available = True
        except ImportError:
            logger.error("duckduckgo-search not installed")
            self.available = False
        except Exception as e:
            logger.error(f"Failed to init DDGS: {e}")
            self.available = False

    async def search(self, query: str, max_results: int = 5) -> str:
        """
        Perform a web search and return a formatted string summary.
        Running in executor because DDGS might be sync blocking.
        """
        if not self.available:
            return "❌ Search module not available."

        try:
            import asyncio
            loop = asyncio.get_event_loop()
            
            def _do_search():
                results = []
                # DDGS().text() is a generator
                for r in self.ddgs.text(query, max_results=max_results):
                    results.append(r)
                return results

            # Run in thread pool to avoid blocking async loop
            results: List[Dict] = await loop.run_in_executor(None, _do_search)
            
            if not results:
                return f"🔍 По запросу '{query}' ничего не найдено."
            
            # Format results
            response = f"🔍 **Результаты поиска:** '{query}'\n\n"
            for i, r in enumerate(results, 1):
                title = r.get('title', 'No Title')
                link = r.get('href', '#')
                body = r.get('body', '')
                response += f"{i}. [{title}]({link})\n_{body}_\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return f"❌ Ошибка поиска: {e}"
