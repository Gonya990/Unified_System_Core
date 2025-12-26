from aios_client import AIOSClient
import json

client = AIOSClient()
print("--- Testing browser_goto with explicit tools ---")

# Define the tool schema for browser_goto
tools = [
    {
        "type": "function",
        "function": {
            "name": "browser_goto",
            "description": "Navigate to a URL using a headless browser",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to navigate to"
                    }
                },
                "required": ["url"]
            }
        }
    }
]

result = client.query("test_agent", "llm", {
    "messages": [
        {"role": "user", "content": "Use the browser_goto tool to visit https://www.google.com and let me know if it was successful."}
    ],
    "llms": [{"name": "gemini-2.0-flash-exp", "provider": "gemini"}],
    "tools": tools
})
print(json.dumps(result, indent=2))
