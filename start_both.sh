#!/bin/bash

# Start Both Backend and Frontend
# This script starts both the FastAPI backend and Next.js frontend

echo "🚀 Starting TalentHub Application..."
echo ""
echo "This will start:"
echo "  - Backend (FastAPI) on http://localhost:8000"
echo "  - Frontend (Next.js) on http://localhost:3000"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend in background
echo "📡 Starting Backend..."
python -m uvicorn app.main:app --reload &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend in background
echo "🎨 Starting Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Services started!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for processes
wait
