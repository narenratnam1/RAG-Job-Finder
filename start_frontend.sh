#!/bin/bash

# Start Frontend Development Server
# This script starts the Next.js frontend on port 3000

echo "🚀 Starting TalentHub Frontend..."
echo ""

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Start the development server
echo "✅ Starting Next.js development server on http://localhost:3000"
echo ""
npm run dev
