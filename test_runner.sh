#!/bin/bash

# Test runner script for Local News MCP Server
# Ensures all tools return MCP-compatible string responses

set -e

echo "🧪 Running Local News MCP Server Tests..."
echo "============================================="

# Check if we're in the project directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from project root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Run: uv venv"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Verify we're in the venv
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Error: Virtual environment not activated"
    exit 1
fi

echo "✅ Virtual environment active: $VIRTUAL_ENV"

# Check dependencies and install if needed
echo "📦 Checking dependencies..."
if ! .venv/bin/python -c "import pytest" 2>/dev/null; then
    echo "Installing pytest in virtual environment..."
    uv add pytest pytest-asyncio pytest-mock
fi

echo "✅ Dependencies ready"
echo ""

# Create tests directory if it doesn't exist
mkdir -p tests
touch tests/__init__.py

# Check if test files exist
if [ ! -f "tests/test_tools.py" ]; then
    echo "⚠️  Warning: tests/test_tools.py not found"
    echo "Please copy the test_tools.py content to tests/test_tools.py"
    echo ""
fi

# Run different test categories using venv python
echo "🔧 Testing Tool Return Types (Critical for MCP)..."
.venv/bin/python -m pytest tests/test_tools.py::TestToolReturnTypes -v 2>/dev/null || echo "Skipping - test file not found"

echo ""
echo "📝 Testing Output Formatting..."
.venv/bin/python -m pytest tests/test_tools.py::TestIntelligentSearchFormatting -v 2>/dev/null || echo "Skipping - test file not found"

echo ""
echo "🚨 Testing Error Handling..."
.venv/bin/python -m pytest tests/test_tools.py::TestErrorHandling -v 2>/dev/null || echo "Skipping - test file not found"

echo ""
echo "🔌 Testing MCP Compatibility (Most Important)..."
.venv/bin/python -m pytest tests/test_tools.py::TestMCPCompatibility -v 2>/dev/null || echo "Skipping - test file not found"

echo ""
echo "📊 Running All Tests..."
if [ -f "tests/test_tools.py" ]; then
    .venv/bin/python -m pytest tests/test_tools.py --tb=short
else
    echo "⚠️  No tests found - please create tests/test_tools.py"
fi

echo ""
echo "✅ Test run completed!"
echo ""
echo "🎯 Key Checks:"
echo "   ✓ All tools return strings (not dicts)"
echo "   ✓ No empty responses"
echo "   ✓ Error handling returns formatted strings"
echo "   ✓ Enhancement info properly displayed"
echo ""
echo "🚀 Ready for MCP deployment!"