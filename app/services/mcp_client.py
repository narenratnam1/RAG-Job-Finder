"""
MCP client: connects to an MCP server over Streamable HTTP (same protocol as FastMCP.streamable_http_app).

When `register_mcp_http_client_app(app)` has been called and the target URL is localhost,
the client uses an in-process httpx ASGITransport (no TCP). Set env MCP_FORCE_HTTP_CLIENT=1
to always use a real HTTP client (e.g. remote MCP server or explicit localhost TCP).
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from urllib.parse import urlparse

import httpx
import mcp.types as types
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from app.core.config import settings

_asgi_app: Any | None = None


def register_mcp_http_client_app(app: Any) -> None:
    """Wire the MCP client to this FastAPI app for in-process Streamable HTTP calls."""
    global _asgi_app
    _asgi_app = app


def _force_http_client() -> bool:
    return os.environ.get("MCP_FORCE_HTTP_CLIENT", "").lower() in ("1", "true", "yes")


def _use_inprocess_transport(url: str) -> bool:
    if _asgi_app is None or _force_http_client():
        return False
    host = urlparse(url).hostname
    return host in ("127.0.0.1", "localhost", None, "")


def call_tool_result_to_text(result: types.CallToolResult) -> str:
    """Flatten MCP tool result content blocks to a single string."""
    parts: list[str] = []
    for block in result.content:
        if isinstance(block, types.TextContent):
            parts.append(block.text)
        else:
            parts.append(block.model_dump_json())
    if result.isError:
        return "Error: " + ("\n".join(parts) if parts else "unknown")
    return "\n".join(parts) if parts else ""


@asynccontextmanager
async def mcp_client_session(
    url: str | None = None,
) -> AsyncIterator[ClientSession]:
    """
    Yields an initialized ClientSession connected to the Streamable HTTP MCP endpoint.
    """
    raw = (url or settings.MCP_STREAMABLE_HTTP_URL).strip()
    # Starlette redirects /mcp -> /mcp/; Streamable HTTP POST must use the final path
    base = raw.rstrip("/")
    if base.endswith("/mcp"):
        base = base + "/"
    client_info = types.Implementation(name="agentic-rag-api", version=settings.APP_VERSION)

    if _use_inprocess_transport(base):
        origin = base.split("/mcp")[0] if "/mcp" in base else base.rstrip("/")
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=_asgi_app),
            base_url=origin,
        ) as http_client:
            async with streamable_http_client(base, http_client=http_client) as (read_stream, write_stream, _get_id):
                async with ClientSession(read_stream, write_stream, client_info=client_info) as session:
                    await session.initialize()
                    yield session
    else:
        async with streamable_http_client(base) as (read_stream, write_stream, _get_id):
            async with ClientSession(read_stream, write_stream, client_info=client_info) as session:
                await session.initialize()
                yield session


async def list_mcp_tools(url: str | None = None) -> types.ListToolsResult:
    async with mcp_client_session(url) as session:
        return await session.list_tools()


async def call_mcp_tool(
    name: str,
    arguments: dict[str, Any] | None = None,
    *,
    url: str | None = None,
) -> types.CallToolResult:
    async with mcp_client_session(url) as session:
        return await session.call_tool(name, arguments or {})
