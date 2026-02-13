from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()


def test_agno_providers():
    print("🚀 Testing Agno Multi-Provider Abstraction\n")

    # 1. OpenAI Agent
    print("--- 🤖 Provider: OpenAI ---")
    openai_agent = Agent(
        model=OpenAIChat(id="gpt-4o"), description="You are a helpful assistant powered by OpenAI.", markdown=True
    )
    openai_agent.print_response("What is the capital of France?", stream=False)
    print("\n")

    # 2. Gemini Agent
    print("--- ♊ Provider: Gemini ---")
    gemini_agent = Agent(
        model=Gemini(id="gemini-1.5-flash"),
        description="You are a helpful assistant powered by Google Gemini.",
        markdown=True,
    )
    gemini_agent.print_response("What is the capital of Israel?", stream=False)
    print("\n")

    # 3. Agent with Tools (Abstraction in action)
    print("--- 🔍 Provider: OpenAI + Search Tool ---")
    search_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGo()],
        description="You are a research agent.",
        show_tool_calls=True,
        markdown=True,
    )
    search_agent.print_response("Latest news about NVIDIA NIM and VS Code integration", stream=False)


if __name__ == "__main__":
    test_agno_providers()
