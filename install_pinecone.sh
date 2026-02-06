#!/bin/bash

# Pinecone Installation Script
# Run this to install the modern Pinecone SDK

echo "=================================="
echo "PINECONE INSTALLATION SCRIPT"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please create one first: python3 -m venv venv"
    exit 1
fi

echo "✓ Found virtual environment"
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Uninstall old package
echo ""
echo "🗑️  Uninstalling old pinecone-client (if present)..."
pip uninstall -y pinecone-client 2>/dev/null || echo "   (not installed, skipping)"

# Install new Pinecone SDK
echo ""
echo "📦 Installing modern Pinecone SDK..."
pip install pinecone

# Verify installation
echo ""
echo "🔍 Verifying installation..."
if pip show pinecone > /dev/null 2>&1; then
    echo "✅ Pinecone SDK installed successfully!"
    echo ""
    pip show pinecone | grep -E "Name|Version"
else
    echo "❌ Installation failed!"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ INSTALLATION COMPLETE!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run migration script: python migrate_to_pinecone.py"
echo "2. This will create your Pinecone index and optionally migrate data"
echo "3. Start your app: python start.py"
echo ""
echo "For detailed instructions, see: PINECONE_MIGRATION_GUIDE.md"
echo ""
