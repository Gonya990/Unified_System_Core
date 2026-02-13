import asyncio

from copilot import CopilotClient


async def test_basic_sdk():
    """Test basic SDK functionality"""
    print("🔧 Testing Copilot SDK...")

    client = CopilotClient()
    await client.start()

    session = await client.create_session({"model": "gpt-4o"})

    done = asyncio.Event()

    def on_event(event):
        if event.type.value == "assistant.message":
            print(f"✅ Copilot: {event.data.content}")
        elif event.type.value == "session.idle":
            done.set()

    session.on(on_event)

    await session.send({"prompt": "What is 2+2? Answer briefly."})
    await done.wait()

    await session.destroy()
    await client.stop()

    print("✅ SDK test passed!")


if __name__ == "__main__":
    asyncio.run(test_basic_sdk())
