#!/bin/bash

# Run script for Agentic RAG API

echo ""
echo "🚀 Agentic RAG API Startup Script"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please run setup first:"
    echo "  ./setup_env.sh"
    echo ""
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate
echo ""

# Run verification
python verify_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🌐 Starting FastAPI server..."
    echo ""
    echo "   🔗 API: http://localhost:8000"
    echo "   📖 Docs: http://localhost:8000/docs"
    echo "   🔧 MCP: http://localhost:8000/mcp"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo ""
    echo "❌ Setup verification failed!"
    echo ""
    echo "To fix, run:"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi
