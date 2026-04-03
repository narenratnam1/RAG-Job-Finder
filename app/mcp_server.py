"""
FastMCP setup: tool registration and Streamable HTTP ASGI app.

``main`` calls ``build_mcp(vector_service)`` and mounts the returned app at ``/mcp``.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from app.services.vector_store import VectorService

logger = logging.getLogger(__name__)


def _screen_candidate_logic(job_description: str, vector_service: VectorService) -> str:
    """Build resume context + task text for screening (shared MCP tool implementation)."""
    try:
        results = vector_service.search(query=job_description, k=10)
        if not results:
            return "No resume information found in the database. Please upload a resume first."

        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Part {i} - Page {result['metadata'].get('page', 'N/A')}]:\n{result['text']}"
            )
        context_section = "\n\n".join(context_parts)
        return f"""CONTEXT: Here are the relevant parts of the candidate's resume:

{context_section}

TASK: Compare the resume parts above against this Job Description:

{job_description}"""
    except Exception as e:
        return f"Error screening candidate: {str(e)}"


def build_mcp(vector_service: VectorService) -> tuple[Any | None, Any | None]:
    """
    Create FastMCP with tools bound to ``vector_service``.

    Returns:
        ``(mcp, mcp_http_app)`` where either may be ``None`` if MCP is not installed.
    """
    try:
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("AgentPolicy", streamable_http_path="/")

        @mcp.tool()
        def consult_policy_db(query: str) -> str:
            """Consult the policy database using semantic search."""
            try:
                results = vector_service.search(query=query, k=3)
                if not results:
                    return "No relevant policy information found."
                formatted_output = f"Found {len(results)} relevant policy documents:\n\n"
                for i, result in enumerate(results, 1):
                    formatted_output += f"--- Result {i} ---\n"
                    formatted_output += f"Source: {result['metadata'].get('source', 'Unknown')}\n"
                    formatted_output += f"Page: {result['metadata'].get('page', 'N/A')}\n"
                    formatted_output += f"Relevance Score: {1 - result['distance']:.4f}\n"
                    formatted_output += f"Content:\n{result['text']}\n\n"
                return formatted_output
            except Exception as e:
                return f"Error querying policy database: {str(e)}"

        @mcp.tool()
        def screen_candidate(job_description: str) -> str:
            """Screen a candidate by comparing their resume against a job description."""
            return _screen_candidate_logic(job_description, vector_service)

        @mcp.tool()
        def get_screener_instructions() -> str:
            """Instructions for using the candidate screening tool."""
            return (
                '1. Upload a PDF Resume. 2. In the chat, paste the Job Description and ask: '
                '"Evaluate this candidate for this role."'
            )

        logger.info(
            "✓ MCP tools registered: consult_policy_db, screen_candidate, get_screener_instructions"
        )
        return mcp, mcp.streamable_http_app()
    except ImportError:
        logger.warning("⚠️  MCP not available - running without MCP tools")
        return None, None


@asynccontextmanager
async def mcp_lifespan(mcp: Any | None) -> AsyncIterator[None]:
    """Run FastMCP session manager for the app lifetime when MCP is enabled."""
    if mcp is not None:
        async with mcp.session_manager.run():
            yield
    else:
        yield
