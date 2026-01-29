import json

from aios_client import AIOSClient

client = AIOSClient()
print("--- Testing Vasya via AIOS ---")

# Define the tool schema for vasya_query
tools = [
    {
        "type": "function",
        "function": {
            "name": "vasya_query",
            "description": "Query Vasya research assistant for structured results",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The research query"
                    }
                },
                "required": ["prompt"]
            }
        }
    }
]

result = client.query("test_agent", "llm", {
    "messages": [
        {"role": "user", "content": "Use the vasya_query tool to find resources about Docker containers."}
    ],
    "llms": [{"name": "gemini-2.0-flash-exp", "provider": "gemini"}],
    "tools": tools
})
print(json.dumps(result, indent=2))
