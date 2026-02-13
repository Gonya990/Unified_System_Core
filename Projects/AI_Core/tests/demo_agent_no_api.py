"""
Mock agent demonstration - работает БЕЗ API ключей

Демонстрирует работу агентной системы с моками вместо реальных LLM.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.tools.file_ops import FileListTool, FileOpsTool
from agents.tools.home_assistant import HomeAssistantTool


async def demo_file_ops():
    """Демо файловых операций без LLM"""
    print("=" * 70)
    print("📁 DEMO: File Operations Tool")
    print("=" * 70)

    file_list = FileListTool()
    file_ops = FileOpsTool()

    # Test 1: List directory
    print("\n🧪 Test: List agent source directory\n")
    path = "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src/agents/"
    result = await file_list.handler(path)
    print(result)

    # Test 2: Read file
    print("\n" + "=" * 70)
    print("\n🧪 Test: Read __init__.py\n")
    file_path = path + "__init__.py"
    result = await file_ops.handler(file_path, max_chars=500)
    print(result)

    print("\n" + "=" * 70)


async def demo_home_assistant():
    """Демо Home Assistant без реального подключения"""
    print("\n" + "=" * 70)
    print("🏠 DEMO: Home Assistant Tool")
    print("=" * 70)

    ha = HomeAssistantTool()

    print("\n📊 Tool Definition:")
    definition = ha.get_definition()
    print(f"Name: {definition['name']}")
    print(f"Description: {definition['description']}")
    print(f"Parameters: {list(definition['parameters']['properties'].keys())}")

    print("\n✅ Tool готов к использованию с реальным Home Assistant")
    print("   (требуется HA_TOKEN в .env)")

    print("\n" + "=" * 70)


async def demo_agent_concept():
    """Демо концепции агента"""
    print("\n" + "=" * 70)
    print("🤖 DEMO: Agent Concept (Function Calling)")
    print("=" * 70)

    print("""
┌─────────────────────────────────────────────────────────────────┐
│                   AI AGENT ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User: "List files in my agents folder"                        │
│    │                                                             │
│    ▼                                                             │
│  ┌──────────────────┐                                           │
│  │  Agent (LLM)     │  ◄─ OpenAI/Gemini/Claude                 │
│  └────────┬─────────┘                                           │
│           │                                                     │
│           │ Decision: Need to call file_list tool              │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐                                           │
│  │  Tool Registry   │                                           │
│  └────────┬─────────┘                                           │
│           │                                                     │
│           ├──► file_list(path="/...")                          │
│           ├──► file_read(path="/...")                          │
│           ├──► control_device(entity="light.room")             │
│           └──► send_email(to="...", subject="...")             │
│                                                                 │
│  Results returned to Agent ─► Final Response to User           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

✅ Что уже реализовано:
  • AgentOrchestrator класс (OpenAI/Gemini)
  • Tool Registration система
  • File Operations (read, list)
  • Home Assistant интеграция
  • Conversation memory
  • Error handling

⚠️  Что нужно для тестирования:
  • Действующий API ключ (OpenAI или Gemini)
  • Или использовать Ollama локально (free!)

📋 Следующие шаги:
  1. Получить новый API ключ ИЛИ настроить Ollama
  2. Добавить MCP Mail tool
  3. Интегрировать с Telegram ботом
  4. Добавить Git operations tool
  5. Production deployment

""")

    print("=" * 70)


async def main():
    """Run all demos"""
    try:
        await demo_file_ops()
        await demo_home_assistant()
        await demo_agent_concept()

        print("\n✅ Демонстрация завершена!")
        print("\n💡 TIP: Обновите API ключи в .env для полного тестирования")
        print("   Или установите Ollama для локальной работы (бесплатно)")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
