#!/usr/bin/env python3
"""
Sovereign Browser Research Agent using Google Antigravity (AGY) SDK
and chrome-devtools-mcp for browser automation.
"""

import argparse
import asyncio
import os
import sys

# Append AI_Core source path to import TokenBroker
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

try:
    from token_broker import TokenBroker
except ImportError:
    print("Error: Could not import TokenBroker. Ensure you are running this from AI_Core or the root directory.")
    sys.exit(1)

try:
    from google.antigravity import Agent, LocalAgentConfig, types
    from google.antigravity.hooks import policy
except ImportError:
    print("Error: google-antigravity SDK is not installed in the active environment.")
    sys.exit(1)


async def main():
    parser = argparse.ArgumentParser(
        description="Run the Antigravity Browser Agent to perform a web research task."
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="The starting URL for the browser agent.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="The goal/prompt for the browser research task.",
    )
    args = parser.parse_args()

    # 1. Retrieve Gemini API Key via TokenBroker
    print("🔑 Initializing TokenBroker and fetching Gemini API Key...")
    broker = TokenBroker()
    api_key = broker.get_key("gemini")
    if not api_key:
        print("❌ Error: Failed to retrieve Gemini API Key from TokenBroker.")
        sys.exit(1)
    print("✓ Gemini API Key successfully fetched.")

    # 2. Configure Agent with chrome-devtools-mcp stdio transport
    print("🚀 Configuring Antigravity Agent with Chrome DevTools MCP server...")
    mcp_servers = [
        types.McpStdioServer(
            name="chrome-devtools",
            command="npx",
            args=["-y", "chrome-devtools-mcp@0.11.0", "--no-usage-statistics"],
        )
    ]

    system_instructions = (
        "You are an expert browser automation and web research assistant. "
        "Your task is to navigate the web, analyze pages, and extract precise information "
        "to satisfy the user's request. You have access to a Chrome browser via the "
        "`chrome-devtools` MCP server tools (e.g. navigate_page, take_snapshot, click, fill, etc.). "
        "Always start by navigating to the user-provided URL, take a snapshot to understand "
        "the structure, and then interact with the page as needed to fulfill the request. "
        "Present your final answer clearly with references/citations to the page contents."
    )

    config = LocalAgentConfig(
        api_key=api_key,
        system_instructions=system_instructions,
        mcp_servers=mcp_servers,
        policies=[policy.allow_all()],  # Allow all browser tools to run
    )

    print(f"🌐 Initiating task: Navigate to '{args.url}' and fulfill: '{args.prompt}'")
    
    # 3. Launch Agent and execute the prompt
    async with Agent(config) as agent:
        chat_prompt = f"Please navigate to this URL: {args.url}\nOnce loaded, perform the following task: {args.prompt}"
        response = await agent.chat(chat_prompt)
        
        print("\n--- Agent Output ---")
        async for chunk in response:
            print(chunk, end="", flush=True)
        print("\n--------------------")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Agent...")
        sys.exit(0)
