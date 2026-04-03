"""
OpenAI tool-calling agent that executes MCP tools via the in-process client
(same behavior as POST /api/mcp/call).
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from app.core.config import settings
from app.services.mcp_client import call_mcp_tool, call_tool_result_to_text

logger = logging.getLogger(__name__)

TOOL_DEFINITIONS_OPENAI: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "consult_policy_db",
            "description": (
                "Search the policy / document knowledge base with semantic search. "
                "Use for HR policy questions, handbook content, or uploaded document RAG."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural-language search query for relevant policy or document chunks.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "screen_candidate",
            "description": (
                "Retrieve resume context from the vector store for the current candidate "
                "and pair it with the given job description for evaluation. "
                "Use when the user wants screening, fit assessment, or compare resume to a role."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "job_description": {
                        "type": "string",
                        "description": "Full job description text to compare against the stored resume.",
                    }
                },
                "required": ["job_description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_screener_instructions",
            "description": (
                "Return step-by-step instructions for how to use the candidate screening flow "
                "(e.g. upload resume, then provide job description)."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]

SYSTEM_PROMPT = """You are a helpful recruiting and policy assistant.
You can call tools to read from the company's policy/document store and to screen candidates against job descriptions.
When a tool returns data, synthesize a clear, conversational answer for the user.
If a tool reports missing data (e.g. no resume uploaded), explain what the user should do next.
"""


def _chat_model() -> str:
    return os.environ.get("AGENT_CHAT_MODEL", settings.LLM_MODEL_NAME)


async def run_agent_chat(
    conversation: list[dict[str, str]],
    *,
    max_tool_rounds: int = 8,
) -> str:
    """
    Run one user-visible turn: ``conversation`` is prior chat (user/assistant only, string content).
    Returns the assistant's final reply text.
    """
    from openai import AsyncOpenAI

    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    model = _chat_model()

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    for m in conversation:
        messages.append({"role": m["role"], "content": m["content"]})

    allowed_tools = frozenset(
        {"consult_policy_db", "screen_candidate", "get_screener_instructions"}
    )

    for _ in range(max_tool_rounds):
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_DEFINITIONS_OPENAI,
            tool_choice="auto",
        )
        choice = response.choices[0]
        msg = choice.message

        if not msg.tool_calls:
            return (msg.content or "").strip()

        messages.append(
            {
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments or "{}",
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
        )

        for tc in msg.tool_calls:
            name = tc.function.name
            try:
                raw_args = tc.function.arguments or "{}"
                args = json.loads(raw_args) if raw_args.strip() else {}
            except json.JSONDecodeError:
                args = {}
            if name not in allowed_tools:
                result = json.dumps({"error": f"Unknown tool: {name}"})
            else:
                try:
                    raw = await call_mcp_tool(name, args)
                    result = call_tool_result_to_text(raw)
                except Exception as e:
                    logger.exception("MCP tool failed in agent chat")
                    result = f"Tool error: {e}"
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                }
            )

    return "[The assistant stopped after too many tool calls. Try a simpler question.]"
