#!/bin/bash

# Setup script for Local News MCP Server testing environment

set -e

echo "🚀 Setting up Local News MCP Server Testing Environment"
echo "======================================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
uv sync

# Install testing dependencies
echo "🧪 Installing testing dependencies..."
pip install pytest pytest-asyncio pytest-mock pytest-cov

# Create tests directory structure
echo "📁 Creating test directory structure..."
mkdir -p tests
mkdir -p tests/unit
mkdir -p tests/integration

# Copy test files to proper locations
if [ -f "test_tools.py" ]; then
    cp test_tools.py tests/test_tools.py
    echo "✅ Copied test_tools.py to tests/"
fi

if [ -f "test_integration.py" ]; then
    cp test_integration.py tests/test_integration.py
    echo "✅ Copied test_integration.py to tests/"
fi

# Make test runner executable
chmod +x test_runner.sh

# Check environment variables
echo "🔑 Checking environment configuration..."
if [ -f ".env" ]; then
    if grep -q "LOCAL_NEWS_API_KEY" .env; then
        echo "✅ API key configuration found"
    else
        echo "⚠️  Warning: LOCAL_NEWS_API_KEY not found in .env"
        echo "   Add your API key: echo 'LOCAL_NEWS_API_KEY=your_key_here' >> .env"
    fi
else
    echo "📝 Creating .env template..."
    cp .env.example .env
    echo "⚠️  Please add your API key to .env file"
fi

# Run initial validation
echo "🔍 Running initial validation..."
python test_integration.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🧪 Next steps:"
echo "1. Add your API key to .env file if not already done"
echo "2. Run tests: ./test_runner.sh"
echo "3. Test with MCP Inspector:"
echo "   npx @modelcontextprotocol/inspector uv --directory . run main.py"
echo "4. Test with Claude Desktop (see README.md for configuration)"
echo ""
echo "🚨 Critical: All tools must return strings for MCP compatibility!"
echo "   This is verified by the test suite."
echo ""

# Display current status
echo "📊 Current Status:"
echo "   Virtual Environment: ✅ Active"
echo "   Dependencies: ✅ Installed"
echo "   Test Structure: ✅ Ready"
echo "   API Key: $([ -f .env ] && grep -q LOCAL_NEWS_API_KEY .env && echo "✅ Configured" || echo "⚠️  Needs setup")"
echo ""
echo "🎯 Ready for development and testing!"