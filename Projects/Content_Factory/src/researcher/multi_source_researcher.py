#!/usr/bin/env python3
"""
Multi-Source Content Researcher
Expands research circle to analyze ALL available sources for script generation.

Sources:
1. Google News (existing)
2. User-provided links (from Reports/research_links.json)
3. YouTube trending
4. Reddit r/technology, r/Futurology
5. Hacker News
6. Wikipedia trending topics
"""

import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()
FACTORY_DIR = SRC_DIR.parent
ROOT_DIR = FACTORY_DIR.parent.parent

sys.path.append(str(SRC_DIR / "researcher"))
sys.path.append(str(ROOT_DIR / "Scripts/Orchestration"))
sys.path.append(str(ROOT_DIR / "Scripts/Research"))

load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

# Import custom modules
try:
    from token_broker import TokenBroker

    BROKER = TokenBroker()
except ImportError:
    BROKER = None

try:
    from agent_mail_client import AgentMailClient

    MAIL_CLIENT = AgentMailClient()
except ImportError:
    MAIL_CLIENT = None

# Configuration
REPORTS_DIR = ROOT_DIR / "Reports"
RESEARCH_LINKS_FILE = REPORTS_DIR / "research_links.json"
TELEGRAM_REPORTS_DIR = REPORTS_DIR
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


class MultiSourceResearcher:
    """Aggregates content ideas from multiple sources"""

    def __init__(self):
        self.openai_key = self._get_key("openai")
        self.client = OpenAI(api_key=self.openai_key) if self.openai_key else None
        self.sources_data = {
            "google_news": [],
            "user_links": [],
            "youtube_trending": [],
            "reddit": [],
            "hackernews": [],
            "wikipedia": [],
        }

    def _get_key(self, provider):
        """Get API key from broker or env"""
        if BROKER:
            k = BROKER.get_key(provider)
            if k:
                return k

        env_map = {
            "openai": "OPENAI_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "serpapi": "SERPAPI_KEY",
        }
        return os.getenv(env_map.get(provider))



    def fetch_user_links(self) -> list[dict]:
        """Load user-provided research links"""
        print("🔗 Fetching user-provided links...")

        if not RESEARCH_LINKS_FILE.exists():
            print("   ⚠️  No research_links.json found")
            print(f"   📝 Create: {RESEARCH_LINKS_FILE}")

            # Create template
            template = {
                "links": [
                    {
                        "url": "https://example.com/article",
                        "category": "AI/Tech/Science",
                        "priority": "high/medium/low",
                        "notes": "Why this is interesting",
                    }
                ],
                "last_updated": datetime.now().isoformat(),
            }
            RESEARCH_LINKS_FILE.write_text(json.dumps(template, indent=2))
            return []

        try:
            data = json.loads(RESEARCH_LINKS_FILE.read_text())
            links = data.get("links", [])

            insights = []
            for link in links:
                # Fetch content from URL
                content = self._fetch_url_content(link["url"])

                insights.append(
                    {
                        "source": "user_link",
                        "url": link["url"],
                        "category": link.get("category", "general"),
                        "priority": link.get("priority", "medium"),
                        "notes": link.get("notes", ""),
                        "content": content[:500] if content else "",
                        "score": {"high": 100, "medium": 50, "low": 10}.get(link.get("priority"), 50),
                    }
                )

            print(f"   ✅ Loaded {len(insights)} user links")
            self.sources_data["user_links"] = insights
            return insights

        except Exception as e:
            print(f"   ❌ User links fetch failed: {e}")
            return []

    def fetch_google_news(self, topics: list[str] = None) -> list[dict]:
        """Fetch Google News RSS (existing functionality)"""
        print("📰 Fetching Google News...")

        if not topics:
            topics = [
                "ai breakthrough 2026",
                "fusion energy progress",
                "mars mission update",
                "quantum computing advancement",
                "renewable energy innovation",
                "medical ai discovery",
                "space exploration milestone",
                "climate tech solution",
            ]

        query = random.choice(topics)
        import urllib.parse

        encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded}+when:1d&hl=en-US&gl=US&ceid=US:en"

        try:
            feed = feedparser.parse(url)
            insights = []

            for entry in feed.entries[:5]:
                insights.append(
                    {
                        "source": "google_news",
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", ""),
                        "score": 30,  # Medium priority
                    }
                )

            print(f"   ✅ Found {len(insights)} news articles")
            self.sources_data["google_news"] = insights
            return insights

        except Exception as e:
            print(f"   ❌ News fetch failed: {e}")
            return []

    def fetch_reddit_trending(self, subreddits: list[str] = None) -> list[dict]:
        """Fetch trending from Reddit"""
        print("🔴 Fetching Reddit trending...")

        if not subreddits:
            subreddits = ["technology", "Futurology", "artificial", "science"]

        insights = []

        for sub in subreddits:
            try:
                url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
                headers = {"User-Agent": USER_AGENT}

                response = requests.get(url, headers=headers, timeout=10)
                data = response.json()

                for post in data["data"]["children"][:5]:
                    p = post["data"]
                    insights.append(
                        {
                            "source": "reddit",
                            "subreddit": sub,
                            "title": p["title"],
                            "url": f"https://reddit.com{p['permalink']}",
                            "upvotes": p.get("ups", 0),
                            "score": min(p.get("ups", 0) / 100, 100),  # Normalize score
                        }
                    )

            except Exception as e:
                print(f"   ⚠️  r/{sub} failed: {e}")

        print(f"   ✅ Found {len(insights)} Reddit posts")
        self.sources_data["reddit"] = insights
        return insights

    def fetch_hackernews(self) -> list[dict]:
        """Fetch Hacker News top stories"""
        print("🟠 Fetching Hacker News...")

        try:
            # Get top story IDs
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
            story_ids = response.json()[:10]

            insights = []
            for sid in story_ids:
                story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5)
                story = story_response.json()

                if story and story.get("type") == "story":
                    insights.append(
                        {
                            "source": "hackernews",
                            "title": story.get("title"),
                            "url": story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                            "score": min(story.get("score", 0) / 10, 100),
                        }
                    )

            print(f"   ✅ Found {len(insights)} HN stories")
            self.sources_data["hackernews"] = insights
            return insights

        except Exception as e:
            print(f"   ❌ HN fetch failed: {e}")
            return []

    def fetch_wikipedia_trending(self) -> list[dict]:
        """Fetch Wikipedia trending topics"""
        print("📚 Fetching Wikipedia trending...")

        try:
            # Get most viewed articles
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")
            url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yesterday}"
            headers = {"User-Agent": USER_AGENT}

            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            insights = []
            articles = data.get("items", [{}])[0].get("articles", [])

            for article in articles[:10]:
                # Skip meta pages
                if article["article"].startswith("Main_Page") or article["article"].startswith("Special:"):
                    continue

                insights.append(
                    {
                        "source": "wikipedia",
                        "title": article["article"].replace("_", " "),
                        "url": f"https://en.wikipedia.org/wiki/{article['article']}",
                        "views": article.get("views", 0),
                        "score": min(article.get("views", 0) / 10000, 100),
                    }
                )

            print(f"   ✅ Found {len(insights)} trending wiki topics")
            self.sources_data["wikipedia"] = insights
            return insights

        except Exception as e:
            print(f"   ❌ Wikipedia fetch failed: {e}")
            return []

    def _fetch_url_content(self, url: str) -> str:
        """Extract text content from URL"""
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()

            text = " ".join(soup.get_text(separator=" ").split())
            return text[:3000]

        except Exception as e:
            print(f"   ⚠️  Failed to fetch {url}: {e}")
            return ""

    def aggregate_all_sources(self) -> list[dict]:
        """Fetch from all sources and aggregate"""
        print("\n🔍 MULTI-SOURCE RESEARCH AGGREGATION")
        print("=" * 60)

        all_insights = []

        # Fetch from all sources

        all_insights.extend(self.fetch_user_links())
        all_insights.extend(self.fetch_google_news())
        all_insights.extend(self.fetch_reddit_trending())
        all_insights.extend(self.fetch_hackernews())
        all_insights.extend(self.fetch_wikipedia_trending())

        # Sort by score (relevance)
        all_insights.sort(key=lambda x: x.get("score", 0), reverse=True)

        print(f"\n📊 TOTAL INSIGHTS: {len(all_insights)}")

        print(f"   User Links: {len(self.sources_data['user_links'])}")
        print(f"   Google News: {len(self.sources_data['google_news'])}")
        print(f"   Reddit: {len(self.sources_data['reddit'])}")
        print(f"   Hacker News: {len(self.sources_data['hackernews'])}")
        print(f"   Wikipedia: {len(self.sources_data['wikipedia'])}")

        return all_insights

    def generate_script_ideas(self, insights: list[dict], count: int = 5) -> list[dict]:
        """Use OpenAI to generate script ideas from aggregated insights"""
        print(f"\n🎬 Generating {count} script ideas from insights...")

        if not self.client:
            print("   ❌ OpenAI client not available")
            return []

        # Prepare context from top insights
        top_insights = insights[:20]
        context = "\n\n".join(
            [
                f"SOURCE: {i['source']}\n"
                f"TITLE: {i.get('title', i.get('text', '')[:100])}\n"
                f"SCORE: {i.get('score', 0)}\n"
                f"URL: {i.get('url', i.get('link', 'N/A'))}"
                for i in top_insights
            ]
        )

        prompt = f"""Based on these trending topics and insights from multiple sources, generate {count} compelling video script ideas.

INSIGHTS:
{context}

For each idea, provide:
1. **Title**: Catchy, viral-worthy title
2. **Hook**: First 5 seconds (Nikolashin style: warning/listicle)
3. **Key Points**: 3-5 main talking points
4. **Source Mix**: Which sources inspired this (Telegram/Reddit/News/etc.)
5. **Viral Potential**: Why this will get views (1-10 score)

Focus on:
- "Peace & Tech" theme (no war/politics)
- Free tool access / hacks (high engagement)
- Practical, actionable insights
- Mix of trending + evergreen

Output as JSON array."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a viral content strategist analyzing multi-source research data.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
            )

            content = response.choices[0].message.content

            # Extract JSON
            import re

            json_match = re.search(r"\[.*\]", content, re.DOTALL)
            if json_match:
                ideas = json.loads(json_match.group())
                print(f"   ✅ Generated {len(ideas)} script ideas")
                return ideas
            else:
                print("   ⚠️  No JSON found in response")
                return []

        except Exception as e:
            print(f"   ❌ Script generation failed: {e}")
            return []

    def save_research_report(self, insights: list[dict], ideas: list[dict]):
        """Save research results to Reports"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = REPORTS_DIR / f"multi_source_research_{timestamp}.json"

        report = {
            "timestamp": datetime.now().isoformat(),
            "sources_summary": {

                "user_links": len(self.sources_data["user_links"]),
                "google_news": len(self.sources_data["google_news"]),
                "reddit": len(self.sources_data["reddit"]),
                "hackernews": len(self.sources_data["hackernews"]),
                "wikipedia": len(self.sources_data["wikipedia"]),
            },
            "total_insights": len(insights),
            "top_insights": insights[:20],
            "script_ideas": ideas,
            "sources_data": self.sources_data,
        }

        report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"\n💾 Research report saved: {report_file.name}")

        # Send via Agent Mail
        if MAIL_CLIENT and MAIL_CLIENT.health_check():
            summary = f"""# Multi-Source Research Complete

**Timestamp**: {datetime.now().isoformat()}

## Sources Analyzed:

- User Links: {len(self.sources_data["user_links"])} URLs
- Google News: {len(self.sources_data["google_news"])} articles
- Reddit: {len(self.sources_data["reddit"])} posts
- Hacker News: {len(self.sources_data["hackernews"])} stories
- Wikipedia: {len(self.sources_data["wikipedia"])} trending topics

**Total Insights**: {len(insights)}
**Script Ideas Generated**: {len(ideas)}

**Top 3 Ideas**:
{chr(10).join([f"{i + 1}. {idea.get('title', 'N/A')}" for i, idea in enumerate(ideas[:3])])}

**Report**: `Reports/{report_file.name}`
"""

            try:
                MAIL_CLIENT.broadcast(
                    subject="🔍 Multi-Source Research Complete",
                    body_md=summary,
                    importance="normal",
                )
                print("   ✅ Sent via Agent Mail")
            except Exception:
                print("   ⚠️  Agent Mail send failed")

        return report_file


def main():
    """Run multi-source research"""
    researcher = MultiSourceResearcher()

    # Aggregate all sources
    insights = researcher.aggregate_all_sources()

    # Generate script ideas
    ideas = researcher.generate_script_ideas(insights, count=5)

    # Save report
    researcher.save_research_report(insights, ideas)

    # Display top ideas
    print("\n🎯 TOP SCRIPT IDEAS:")
    print("=" * 60)
    for i, idea in enumerate(ideas, 1):
        print(f"\n{i}. {idea.get('title', 'N/A')}")
        print(f"   Hook: {idea.get('hook', 'N/A')[:100]}...")
        print(f"   Viral Score: {idea.get('viral_potential', 'N/A')}/10")

    print("\n✅ Multi-source research complete!")


if __name__ == "__main__":
    main()
