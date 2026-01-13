
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()

def test_agno_ultra_basic():
    print("🚀 Testing Agno Ultra Basic\n")

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        markdown=True
    )
    agent.print_response("Say 'Agno is working' in Russian")

if __name__ == "__main__":
    test_agno_ultra_basic()
