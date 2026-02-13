"""
Gemini-based Agent Orchestrator

Use Google Gemini API instead of OpenAI for function calling.
"""

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional

import google.generativeai as genai

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """Tool definition for function calling"""

    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable
    requires_approval: bool = False


class GeminiAgentOrchestrator:
    """
    Agent orchestration using Google Gemini with function calling.
    """

    SYSTEM_PROMPT = """You are a helpful AI agent with access to tools.

When given a task:
1. Break it down into clear steps
2. Use available tools to accomplish each step
3. Combine results to give final answer

Always explain your reasoning before using tools.
If a task is ambiguous, ask for clarification before proceeding.
Be concise and direct in your responses."""

    def __init__(self, model: str = "gemini-2.0-flash-exp", api_key: Optional[str] = None):
        """Initialize Gemini Agent"""
        api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY must be set")

        genai.configure(api_key=api_key)
        self.model_name = model
        self.tools: dict[str, Tool] = {}
        self.conversation_history: list[dict] = []

    def register_tool(self, tool: Tool):
        """Register a tool"""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def _build_gemini_tools(self) -> list[genai.protos.Tool]:
        """Convert tools to Gemini format"""
        if not self.tools:
            return []

        # Convert OpenAI-style JSON Schema to Gemini function declarations
        function_declarations = []
        for tool in self.tools.values():
            # Convert schema
            gemini_params = self._convert_schema_to_gemini(tool.parameters)

            function_declarations.append(
                genai.protos.FunctionDeclaration(name=tool.name, description=tool.description, parameters=gemini_params)
            )

        return [genai.protos.Tool(function_declarations=function_declarations)]

    def _convert_schema_to_gemini(self, openai_schema: dict[str, Any]) -> genai.protos.Schema:
        """Convert OpenAI JSON Schema to Gemini Schema"""
        properties = {}
        required = openai_schema.get("required", [])

        for prop_name, prop_def in openai_schema.get("properties", {}).items():
            prop_type = prop_def.get("type", "string")

            # Map JSON types to Gemini types
            type_mapping = {
                "string": genai.protos.Type.STRING,
                "integer": genai.protos.Type.INTEGER,
                "number": genai.protos.Type.NUMBER,
                "boolean": genai.protos.Type.BOOLEAN,
                "array": genai.protos.Type.ARRAY,
                "object": genai.protos.Type.OBJECT,
            }

            gemini_type = type_mapping.get(prop_type, genai.protos.Type.STRING)

            properties[prop_name] = genai.protos.Schema(type=gemini_type, description=prop_def.get("description", ""))

        return genai.protos.Schema(type=genai.protos.Type.OBJECT, properties=properties, required=required)

    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool"""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"

        tool = self.tools[tool_name]

        try:
            logger.info(f"Executing tool: {tool_name} with args: {arguments}")
            result = await tool.handler(**arguments)

            if isinstance(result, dict):
                return json.dumps(result, indent=2)
            return str(result)

        except Exception as e:
            logger.error(f"Tool execution error: {e}", exc_info=True)
            return f"Error executing {tool_name}: {str(e)}"

    async def run(
        self, user_message: str, on_progress: Optional[Callable[[str], None]] = None, max_iterations: int = 10
    ) -> str:
        """Run agent with Gemini"""

        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                tools=self._build_gemini_tools() if self.tools else None,
                system_instruction=self.SYSTEM_PROMPT,
            )

            iterations = 0
            chat = model.start_chat(history=[])

            while iterations < max_iterations:
                iterations += 1
                logger.info(f"Iteration {iterations}/{max_iterations}")

                if iterations == 1:
                    response = chat.send_message(user_message)
                else:
                    response = chat.send_message("Continue")

                # Check for function calls
                if hasattr(response, "candidates") and response.candidates:
                    candidate = response.candidates[0]

                    if hasattr(candidate.content, "parts"):
                        function_calls = [part for part in candidate.content.parts if hasattr(part, "function_call")]

                        if function_calls:
                            # Execute function calls
                            for fc_part in function_calls:
                                fc = fc_part.function_call
                                tool_name = fc.name
                                arguments = dict(fc.args)

                                if on_progress:
                                    on_progress(f"🔧 Executing: {tool_name}")

                                result = await self.execute_tool(tool_name, arguments)

                                # Send result back
                                response = chat.send_message(
                                    genai.protos.Content(
                                        parts=[
                                            genai.protos.Part(
                                                function_response=genai.protos.FunctionResponse(
                                                    name=tool_name, response={"result": result}
                                                )
                                            )
                                        ]
                                    )
                                )
                            continue

                # No more function calls, return final response
                return response.text

            return f"⚠️ Max iterations ({max_iterations}) reached"

        except Exception as e:
            logger.error(f"Gemini error: {e}", exc_info=True)
            return f"❌ Error: {str(e)}"

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("Conversation reset")
