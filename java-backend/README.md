# Java-only API (Option B)

Spring Boot **3.4** + **Spring AI 1.0** with:

- **MCP server** (WebMVC + SSE) — same three tools as the Python app: `consult_policy_db`, `screen_candidate`, `get_screener_instructions`
- **Pinecone** vector store + **OpenAI** `text-embedding-3-small` (1536-d), aligned with the Python stack

## Prerequisites

- **JDK 17+**
- **Maven 3.8+**
- Environment variables: `OPENAI_API_KEY`, `PINECONE_API_KEY`, and optionally `PINECONE_INDEX_NAME` (default `resume-index`)

## Run

```bash
cd java-backend
export OPENAI_API_KEY=...
export PINECONE_API_KEY=...
export PINECONE_INDEX_NAME=resume-index   # optional
mvn spring-boot:run
```

Default HTTP port: **8080** (`PORT` overrides).

## Endpoints

| Purpose | Path |
|--------|------|
| Health | `GET /health` |
| MCP SSE (default Spring AI) | See `spring.ai.mcp.server` — typically **`GET /sse`** for the SSE stream and the message endpoint from config (defaults include **`/mcp/message`**) |

Configure MCP client URLs via `spring.ai.mcp.server.sse-endpoint` and `spring.ai.mcp.server.sse-message-endpoint` in `application.yml`.

This transport is **SSE-based** (Spring AI WebMVC), not the Python FastMCP **Streamable HTTP** path. Point Cursor or other MCP clients at the SSE URL your server exposes.

## Relation to the Python backend

The FastAPI app in `app/` is unchanged. Run **either** the Python API or this Java API for backend + MCP during migration; add PDF upload and remaining REST routes here to reach full parity.
