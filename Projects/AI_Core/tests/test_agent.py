"""
Simple test script for AI Agent system

Tests basic agent functionality with file operations tool.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

from agents.base_agent import AgentOrchestrator, Tool
from agents.tools.file_ops import FileListTool, FileOpsTool
from agents.tools.home_assistant import HomeAssistantTool


async def test_file_ops():
    """Test agent with file operations"""
    print("=" * 60)
    print("🧪 Testing AI Agent with File Operations")
    print("=" * 60)

    # Create agent
    agent = AgentOrchestrator(model="gpt-4o-mini")  # Use mini for testing

    # Register file tools
    file_ops = FileOpsTool()
    agent.register_tool(
        Tool(
            name="file_read",
            description=file_ops.get_definition()["description"],
            parameters=file_ops.get_definition()["parameters"],
            handler=file_ops.handler,
        )
    )

    file_list = FileListTool()
    agent.register_tool(
        Tool(
            name="file_list",
            description=file_list.get_definition()["description"],
            parameters=file_list.get_definition()["parameters"],
            handler=file_list.handler,
        )
    )

    print(f"\n✅ Registered {len(agent.tools)} tools")

    # Test task
    task = "List files in /Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src/agents/"

    print(f"\n📝 Task: {task}\n")

    def progress_callback(msg: str):
        print(f"  {msg}")

    # Run agent
    result = await agent.run(task, on_progress=progress_callback)

    print("\n💬 Agent Response:")
    print(result)
    print("\n" + "=" * 60)


async def test_home_assistant():
    """Test agent with Home Assistant"""
    print("\n" + "=" * 60)
    print("🧪 Testing AI Agent with Home Assistant")
    print("=" * 60)

    agent = AgentOrchestrator(model="gpt-4o-mini")

    # Register HA tool
    ha_tool = HomeAssistantTool()
    agent.register_tool(
        Tool(
            name="control_device",
            description=ha_tool.get_definition()["description"],
            parameters=ha_tool.get_definition()["parameters"],
            handler=ha_tool.handler,
        )
    )

    print("\n✅ Registered Home Assistant tool")

    # Skip test if HA not configured
    import os

    if not os.getenv("HA_TOKEN"):
        print("\n⚠️  Skipping - HA_TOKEN not set")
        return

    task = "Get the state of light.living_room"
    print(f"\n📝 Task: {task}\n")

    result = await agent.run(task)
    print("\n💬 Agent Response:")
    print(result)
    print("\n" + "=" * 60)


async def main():
    """Run all tests"""
    try:
        await test_file_ops()
        await test_home_assistant()

        print("\n✅ All tests completed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
