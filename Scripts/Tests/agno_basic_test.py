
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()

def test_agno_basic():
    print("🚀 Testing Agno with OpenAI\n")

    # OpenAI Agent
    print("--- 🤖 Provider: OpenAI ---")
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        description="You are a helpful assistant powered by OpenAI.",
        markdown=True
    )
    agent.print_response("Say hello in Russian", stream=False)
    print("\n--- ✅ Test Complete ---")

if __name__ == "__main__":
    test_agno_basic()
