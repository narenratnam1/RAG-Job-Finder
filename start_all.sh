#!/bin/bash

# Start both backend and frontend servers

echo "🚀 Starting Agentic RAG API - Full Stack"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run: ./setup_env.sh"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd "$SCRIPT_DIR/frontend"
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Frontend dependencies installation failed"
        exit 1
    fi
    cd "$SCRIPT_DIR"
fi

echo "✅ All dependencies verified"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔵 Starting Backend Server (Port 8000)..."
echo ""

# Start backend in background
cd "$SCRIPT_DIR"
source venv/bin/activate
python start.py &
BACKEND_PID=$!

echo "   Backend PID: $BACKEND_PID"
echo "   Backend URL: http://localhost:8000"
echo ""

# Wait for backend to be ready (Pinecone init can take a few seconds)
echo "⏳ Waiting for backend to be ready..."
sleep 5

# Check if backend is running (retry — Pinecone/OpenAI init can be slow)
BACKEND_OK=0
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        BACKEND_OK=1
        break
    fi
    sleep 1
done
if [ "$BACKEND_OK" -ne 1 ]; then
    echo "❌ Backend failed to become ready on http://localhost:8000/health"
    echo "   Check .env (OPENAI_API_KEY, PINECONE_*), terminal output above, and run: python start.py"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend is ready!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🟢 Starting Frontend Server (Port 3000)..."
echo ""

# Start frontend (Next.js: use `dev`, not `start` — `npm start` runs `next start` and needs `next build` first)
cd "$SCRIPT_DIR/frontend"
BROWSER=none npm run dev &
FRONTEND_PID=$!

echo "   Frontend PID: $FRONTEND_PID"
echo "   Frontend URL: http://localhost:3000"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Full Stack Application Started!"
echo ""
echo "📱 Access the application:"
echo "   🌐 Frontend: http://localhost:3000"
echo "   🔧 Backend:  http://localhost:8000"
echo "   📖 API Docs: http://localhost:8000/docs"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    # Also kill any child processes
    pkill -P $BACKEND_PID 2>/dev/null
    pkill -P $FRONTEND_PID 2>/dev/null
    echo "✅ All servers stopped"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup INT

# Wait for user to stop
wait
