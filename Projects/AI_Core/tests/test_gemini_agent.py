"""
Test script for Gemini Agent

Tests agent with Google Gemini API instead of OpenAI.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv

load_dotenv()

from agents.gemini_agent import GeminiAgentOrchestrator, Tool
from agents.tools.file_ops import FileListTool, FileOpsTool

import pytest


@pytest.mark.asyncio
async def test_gemini_agent():
    """Test Gemini agent with file operations"""
    print("=" * 60)
    print("🧪 Testing Gemini Agent with File Operations")
    print("=" * 60)

    # Create Gemini agent
    agent = GeminiAgentOrchestrator()

    # Register file tools
    file_list = FileListTool()
    agent.register_tool(
        Tool(
            name="file_list",
            description=file_list.get_definition()["description"],
            parameters=file_list.get_definition()["parameters"],
            handler=file_list.handler,
        )
    )

    file_ops = FileOpsTool()
    agent.register_tool(
        Tool(
            name="file_read",
            description=file_ops.get_definition()["description"],
            parameters=file_ops.get_definition()["parameters"],
            handler=file_ops.handler,
        )
    )

    print(f"\n✅ Registered {len(agent.tools)} tools\n")

    # Test task
    task = (
        "List the files in /Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src/agents/ directory"
    )

    print(f"📝 Task: {task}\n")

    def progress(msg):
        print(f"  {msg}")

    # Run agent
    result = await agent.run(task, on_progress=progress)

    print("\n💬 Agent Response:")
    print(result)
    print("\n" + "=" * 60)

    # Test 2: Read a specific file
    print("\n🧪 Test 2: Read file content\n")
    task2 = "Read the file /Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src/agents/__init__.py and tell me what it contains"
    print(f"📝 Task: {task2}\n")

    agent.reset_conversation()
    result2 = await agent.run(task2, on_progress=progress)

    print("\n💬 Agent Response:")
    print(result2)
    print("\n" + "=" * 60)


async def main():
    """Run tests"""
    try:
        await test_gemini_agent()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
