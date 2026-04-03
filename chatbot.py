#!/usr/bin/env python3
"""
Terminal agent that uses an LLM with tool-calling and executes tools via
POST http://127.0.0.1:8000/api/mcp/call

Requires:
  - FastAPI backend on port 8000 with MCP enabled
  - OpenAI: OPENAI_API_KEY (default provider)
  - Anthropic: pip install anthropic, ANTHROPIC_API_KEY, CHATBOT_PROVIDER=anthropic

Env:
  MCP_CALL_URL   — default http://127.0.0.1:8000/api/mcp/call
  CHATBOT_MODEL  — e.g. gpt-4o, gpt-4o-mini, claude-sonnet-4-20250514
  CHATBOT_PROVIDER — openai | anthropic
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

# ---------------------------------------------------------------------------
# Tool schemas (aligned with FastMCP tools in app/main.py)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS_OPENAI = [
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

# Anthropic expects name/description/input_schema at top level
TOOL_DEFINITIONS_ANTHROPIC = [
    {
        "name": "consult_policy_db",
        "description": TOOL_DEFINITIONS_OPENAI[0]["function"]["description"],
        "input_schema": TOOL_DEFINITIONS_OPENAI[0]["function"]["parameters"],
    },
    {
        "name": "screen_candidate",
        "description": TOOL_DEFINITIONS_OPENAI[1]["function"]["description"],
        "input_schema": TOOL_DEFINITIONS_OPENAI[1]["function"]["parameters"],
    },
    {
        "name": "get_screener_instructions",
        "description": TOOL_DEFINITIONS_OPENAI[2]["function"]["description"],
        "input_schema": TOOL_DEFINITIONS_OPENAI[2]["function"]["parameters"],
    },
]

SYSTEM_PROMPT = """You are a helpful recruiting and policy assistant.
You can call tools to read from the company's policy/document store and to screen candidates against job descriptions.
When a tool returns data, synthesize a clear, conversational answer for the user.
If a tool reports missing data (e.g. no resume uploaded), explain what the user should do next.
"""


def mcp_call(url: str, name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    """POST { name, arguments } to the FastAPI MCP bridge; return parsed JSON."""
    payload = json.dumps(
        {"name": name, "arguments": arguments if arguments is not None else {}}
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(body).get("detail", body)
        except json.JSONDecodeError:
            detail = body
        return {
            "error": True,
            "status": e.code,
            "text": f"HTTP {e.code} from MCP API: {detail}",
        }
    except urllib.error.URLError as e:
        return {"error": True, "text": f"Request failed: {e.reason}"}


def tool_result_text(data: dict[str, Any]) -> str:
    if data.get("error"):
        return data.get("text", str(data))
    return data.get("text") or json.dumps(data.get("content"), indent=2)


def run_openai_loop(
    mcp_url: str,
    model: str,
    max_tool_rounds: int = 8,
) -> None:
    from openai import OpenAI

    client = OpenAI()
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    while True:
        try:
            user_line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_line:
            continue
        if user_line.lower() in ("quit", "exit", "q"):
            break

        messages.append({"role": "user", "content": user_line})

        for _ in range(max_tool_rounds):
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=TOOL_DEFINITIONS_OPENAI,
                tool_choice="auto",
            )
            choice = response.choices[0]
            msg = choice.message

            if not msg.tool_calls:
                text = (msg.content or "").strip()
                print(f"Assistant: {text}\n")
                messages.append(
                    {"role": "assistant", "content": msg.content or ""},
                )
                break

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
                if name not in (
                    "consult_policy_db",
                    "screen_candidate",
                    "get_screener_instructions",
                ):
                    result = json.dumps({"error": f"Unknown tool: {name}"})
                else:
                    data = mcp_call(mcp_url, name, args)
                    result = tool_result_text(data)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    }
                )
        else:
            print("Assistant: [Stopped: too many tool rounds]\n")


def run_anthropic_loop(
    mcp_url: str,
    model: str,
    max_tool_rounds: int = 8,
) -> None:
    try:
        import anthropic
    except ImportError:
        print(
            "Anthropic provider selected but package 'anthropic' is not installed. "
            "Run: pip install anthropic",
            file=sys.stderr,
        )
        sys.exit(1)

    client = anthropic.Anthropic()
    conversation: list[dict[str, Any]] = []

    while True:
        try:
            user_line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_line:
            continue
        if user_line.lower() in ("quit", "exit", "q"):
            break

        conversation.append({"role": "user", "content": user_line})

        for _ in range(max_tool_rounds):
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS_ANTHROPIC,
                messages=conversation,
            )

            if response.stop_reason == "tool_use":
                assistant_blocks = []
                tool_result_blocks = []
                for block in response.content:
                    if block.type == "text":
                        assistant_blocks.append({"type": "text", "text": block.text})
                    elif block.type == "tool_use":
                        assistant_blocks.append(
                            {
                                "type": "tool_use",
                                "id": block.id,
                                "name": block.name,
                                "input": block.input,
                            }
                        )
                        name = block.name
                        args = block.input if isinstance(block.input, dict) else {}
                        if name not in (
                            "consult_policy_db",
                            "screen_candidate",
                            "get_screener_instructions",
                        ):
                            out = json.dumps({"error": f"Unknown tool: {name}"})
                        else:
                            data = mcp_call(mcp_url, name, args)
                            out = tool_result_text(data)
                        tool_result_blocks.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": out,
                            }
                        )

                conversation.append({"role": "assistant", "content": assistant_blocks})
                conversation.append({"role": "user", "content": tool_result_blocks})
                continue

            text_parts = [
                b.text for b in response.content if getattr(b, "type", None) == "text"
            ]
            reply = "\n".join(text_parts).strip()
            print(f"Assistant: {reply}\n")
            conversation.append({"role": "assistant", "content": response.content})
            break
        else:
            print("Assistant: [Stopped: too many tool rounds]\n")


def main() -> None:
    mcp_url = os.environ.get(
        "MCP_CALL_URL", "http://127.0.0.1:8000/api/mcp/call"
    ).rstrip("/")
    provider = os.environ.get("CHATBOT_PROVIDER", "openai").lower().strip()

    if provider == "anthropic":
        model = os.environ.get("CHATBOT_MODEL", "claude-sonnet-4-20250514")
        print(f"MCP: {mcp_url} | Provider: Anthropic | Model: {model}\n")
        run_anthropic_loop(mcp_url, model)
    else:
        model = os.environ.get("CHATBOT_MODEL", "gpt-4o-mini")
        print(f"MCP: {mcp_url} | Provider: OpenAI | Model: {model}\n")
        run_openai_loop(mcp_url, model)


if __name__ == "__main__":
    main()
