import asyncio
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append("/home/gonya/Documents/Unified_System/Windows_AI_Core")

from src.web_search import WebSearch
from src.inference_client import InferenceClient
from src.config_manager import ConfigManager

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ResearchAgent")

async def conduct_research():
    logger.info("🕵️ Starting OpenCloud/Router & GPT-5.2 Research...")
    
    # Init Tools
    config = ConfigManager()
    search_tool = WebSearch()
    council = InferenceClient(config)
    
    if not search_tool.available:
        logger.error("❌ Search tool unavailable (Check SERPAPI_KEY).")
        return

    # Questions to research
    queries = [
        "OpenRouter API python integration example github",
        "OpenAI GPT-5.2 release date capabilities",
        "OpenCloud AI model aggregator features"
    ]
    
    compiled_knowledge = ""
    
    for q in queries:
        logger.info(f"🔍 Searching: {q}")
        results = await search_tool.search(q, max_results=3)
        compiled_knowledge += f"\n\n### Query: {q}\n{results}\n"
    
    # Synthesis by Council
    logger.info("🧠 Council is analyzing findings...")
    
    prompt = f"""
    You are the Carpathian Council (AI Consensus System).
    Analyze the following search results about 'OpenRouter', 'OpenCloud', and 'GPT-5.2'.
    
    Search Data:
    {compiled_knowledge}
    
    Your Task:
    1. Explain how to integrate OpenRouter specifically (Endpoint, Auth).
    2. Confirm if GPT-5.2 exists or if it's a future/rumored model.
    3. Define what 'OpenCloud' likely refers to in this context.
    
    output formatted markdown.
    """
    
    # Try OpenAI first since Gemini is hitting limits
    try:
        response, _ = await council._chat_generic("openai", [{"role": "user", "content": prompt}])
        if "[Error" in response:
            logger.warning("OpenAI failed, falling back to Council default...")
            response, _ = await council.chat([{"role": "user", "content": prompt}])
    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        response = "Synthesis failed due to API errors."
    
    logger.info("✅ Research Complete. Saving report...")
    with open("research_results.md", "w") as f:
        f.write("# Research Report: OpenCloud & GPT-5.2\n\n")
        f.write(response)
        
    print(response)

if __name__ == "__main__":
    asyncio.run(conduct_research())
