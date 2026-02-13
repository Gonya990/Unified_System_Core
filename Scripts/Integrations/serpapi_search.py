#!/usr/bin/env python3
"""
SerpAPI Web Search Integration
Provides Google/Bing search results for AI agents
https://serpapi.com
"""

import logging
import os

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SerpAPI")


class SerpAPIClient:
    """
    Client for SerpAPI - Google Search Results API

    Usage:
        client = SerpAPIClient()
        results = client.search("Python best practices 2024")

    Requires SERPAPI_KEY environment variable.
    """

    BASE_URL = "https://serpapi.com/search"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        if not self.api_key:
            logger.warning("SERPAPI_KEY not set. Get one at https://serpapi.com/dashboard")

    def search(
        self,
        query: str,
        engine: str = "google",
        num_results: int = 10,
        location: str = None,
        language: str = "en",
        country: str = None,
    ) -> dict:
        """
        Search the web using SerpAPI

        Args:
            query: Search query
            engine: Search engine (google, bing, yandex, etc)
            num_results: Number of results to return
            location: Location for localized results
            language: Language code (en, ru, he, etc)
            country: Country code (us, il, ru, etc)

        Returns:
            Dict with organic_results, knowledge_graph, etc
        """
        if not self.api_key:
            return {"error": "SERPAPI_KEY not configured"}

        params = {"api_key": self.api_key, "engine": engine, "q": query, "num": num_results, "hl": language}

        if location:
            params["location"] = location
        if country:
            params["gl"] = country

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            data = response.json()

            if "error" in data:
                logger.error(f"SerpAPI error: {data['error']}")
                return {"error": data["error"]}

            # Extract key information
            result = {
                "query": query,
                "organic_results": [],
                "knowledge_graph": data.get("knowledge_graph"),
                "answer_box": data.get("answer_box"),
                "total_results": data.get("search_information", {}).get("total_results"),
            }

            # Parse organic results
            for item in data.get("organic_results", [])[:num_results]:
                result["organic_results"].append(
                    {
                        "title": item.get("title"),
                        "link": item.get("link"),
                        "snippet": item.get("snippet"),
                        "position": item.get("position"),
                    }
                )

            return result

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"error": str(e)}

    def search_images(self, query: str, num_results: int = 10) -> list:
        """Search for images"""
        params = {"api_key": self.api_key, "engine": "google_images", "q": query, "num": num_results}

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            data = response.json()

            return [
                {
                    "title": img.get("title"),
                    "original": img.get("original"),
                    "thumbnail": img.get("thumbnail"),
                    "source": img.get("source"),
                }
                for img in data.get("images_results", [])[:num_results]
            ]
        except Exception as e:
            return [{"error": str(e)}]

    def search_news(self, query: str, num_results: int = 10) -> list:
        """Search for news articles"""
        params = {"api_key": self.api_key, "engine": "google_news", "q": query, "num": num_results}

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            data = response.json()

            return [
                {
                    "title": news.get("title"),
                    "link": news.get("link"),
                    "source": news.get("source", {}).get("name"),
                    "date": news.get("date"),
                    "snippet": news.get("snippet"),
                }
                for news in data.get("news_results", [])[:num_results]
            ]
        except Exception as e:
            return [{"error": str(e)}]


def search_for_ai(query: str, num_results: int = 5) -> str:
    """
    Simple function for AI agents to search the web
    Returns formatted text suitable for LLM context
    """
    client = SerpAPIClient()
    results = client.search(query, num_results=num_results)

    if "error" in results:
        return f"Search failed: {results['error']}"

    output = [f"## Web Search Results for: {query}\n"]

    # Add answer box if present
    if results.get("answer_box"):
        ab = results["answer_box"]
        if ab.get("answer"):
            output.append(f"**Quick Answer:** {ab['answer']}\n")
        elif ab.get("snippet"):
            output.append(f"**Featured Snippet:** {ab['snippet']}\n")

    # Add organic results
    for i, item in enumerate(results.get("organic_results", []), 1):
        output.append(f"\n### {i}. {item['title']}")
        output.append(f"**URL:** {item['link']}")
        if item.get("snippet"):
            output.append(f"{item['snippet']}")

    return "\n".join(output)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python serpapi_search.py <query>")
        print("Example: python serpapi_search.py 'AI trends 2024'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(search_for_ai(query))
