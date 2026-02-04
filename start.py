#!/usr/bin/env python3
"""
Simple startup script for Agentic RAG API
"""

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Agentic RAG API...")
    print("   🔗 API: http://localhost:8000")
    print("   📖 Docs: http://localhost:8000/docs")
    print("   🔧 MCP: http://localhost:8000/mcp")
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
