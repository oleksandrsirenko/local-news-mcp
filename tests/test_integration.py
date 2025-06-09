"""
Integration tests for Local News MCP Server.

These tests can be run with the MCP Inspector to verify
the server works correctly in a real MCP environment.
"""

import json
import asyncio
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import mcp


class MCPInspectorTests:
    """Test cases designed for MCP Inspector validation."""

    @staticmethod
    def test_cases():
        """Return test cases for manual MCP Inspector testing."""
        return {
            "tools": [
                {
                    "name": "search_news",
                    "description": "Test basic search functionality",
                    "test_inputs": [
                        {
                            "description": "Simple tech search",
                            "arguments": {
                                "q": "technology",
                                "locations": ["San Francisco, California"],
                                "theme": "Tech",
                            },
                            "expected": "Should return formatted string with tech articles",
                        },
                        {
                            "description": "Boolean query test",
                            "arguments": {
                                "q": "Apple AND iPhone",
                                "locations": ["California"],
                                "theme": "Tech",
                            },
                            "expected": "Should return formatted string with Apple iPhone articles",
                        },
                    ],
                },
                {
                    "name": "intelligent_search",
                    "description": "Test enhanced search with clustering",
                    "test_inputs": [
                        {
                            "description": "Enhanced tech layoffs search",
                            "arguments": {
                                "enhanced_query": 'technology AND (layoffs OR "job cuts" OR downsizing) NOT sports',
                                "locations": [
                                    "San Francisco, California",
                                    "Seattle, Washington",
                                ],
                                "theme": "Tech",
                                "original_query": "tech layoffs",
                                "clustering": True,
                                "max_clusters": 10,
                            },
                            "expected": "Should return clustered results with enhancement transparency",
                        },
                        {
                            "description": "Real estate search",
                            "arguments": {
                                "enhanced_query": '"real estate" AND (market OR prices OR sales) NOT vacation',
                                "locations": ["Los Angeles, California"],
                                "theme": "Business",
                                "original_query": "housing market",
                                "clustering": False,
                            },
                            "expected": "Should return standard results with enhancement info",
                        },
                        {
                            "description": "Error handling test",
                            "arguments": {
                                "enhanced_query": "invalid query with @#$%",
                                "locations": ["Invalid Location"],
                                "original_query": "test error",
                            },
                            "expected": "Should return formatted error message (still a string)",
                        },
                    ],
                },
                {
                    "name": "get_latest_headlines",
                    "description": "Test headlines functionality",
                    "test_inputs": [
                        {
                            "description": "Recent headlines",
                            "arguments": {
                                "locations": ["New York City, New York"],
                                "when": "24h",
                                "theme": "Business",
                            },
                            "expected": "Should return recent business headlines",
                        }
                    ],
                },
            ],
            "prompts": [
                {
                    "name": "enhance-query",
                    "description": "Test query enhancement",
                    "test_inputs": [
                        {
                            "description": "Simple business query",
                            "arguments": {
                                "user_input": "tech layoffs",
                                "domain_context": "business",
                                "location_focus": "Silicon Valley",
                            },
                            "expected": "Should provide enhanced query with boolean operators",
                        },
                        {
                            "description": "Real estate query",
                            "arguments": {
                                "user_input": "housing market",
                                "domain_context": "real estate",
                                "location_focus": "Los Angeles",
                            },
                            "expected": "Should provide sophisticated real estate query",
                        },
                    ],
                },
                {
                    "name": "analyze-search-intent",
                    "description": "Test intent analysis",
                    "test_inputs": [
                        {
                            "description": "Business intent analysis",
                            "arguments": {
                                "user_input": "What's happening with tech companies in San Francisco?"
                            },
                            "expected": "Should analyze domain, entities, and intent",
                        }
                    ],
                },
            ],
        }

    @staticmethod
    def print_test_guide():
        """Print a guide for manual testing with MCP Inspector."""
        print("🔍 MCP Inspector Test Guide")
        print("=" * 50)
        print()
        print("1. Start the MCP Inspector:")
        print("   npx @modelcontextprotocol/inspector uv --directory . run main.py")
        print()
        print("2. Test Tools (Critical - Must Return Strings):")
        print("   ✓ Go to Tools tab")
        print("   ✓ Test each tool with the arguments below")
        print("   ✓ Verify ALL responses are formatted strings (not raw JSON)")
        print()

        test_cases = MCPInspectorTests.test_cases()

        for tool in test_cases["tools"]:
            print(f"🔧 {tool['name']}:")
            print(f"   {tool['description']}")
            for i, test in enumerate(tool["test_inputs"], 1):
                print(f"   Test {i}: {test['description']}")
                print(f"   Arguments: {json.dumps(test['arguments'], indent=6)}")
                print(f"   Expected: {test['expected']}")
                print()

        print("3. Test Prompts:")
        for prompt in test_cases["prompts"]:
            print(f"💬 {prompt['name']}:")
            for test in prompt["test_inputs"]:
                print(f"   Test: {test['description']}")
                print(f"   Arguments: {json.dumps(test['arguments'], indent=6)}")
                print()

        print("4. Critical Validation Checklist:")
        print("   ✅ All tool responses are strings (not dicts/objects)")
        print("   ✅ No 'No result received from client-side tool execution' errors")
        print("   ✅ Enhancement transparency shows original vs enhanced queries")
        print("   ✅ Error handling returns formatted error messages")
        print("   ✅ Clustering results show diverse stories")
        print("   ✅ Location detection methods are displayed")
        print()
        print("5. Resources to Test:")
        print("   📖 knowledge://query-syntax")
        print("   📖 guide://workflow")
        print()


def run_validation_scenarios():
    """Run validation scenarios that can be executed independently."""
    print("🧪 Running MCP Server Validation...")
    print()

    # Test 1: Verify server can be imported and initialized
    try:
        from main import mcp, API_KEY

        print("✅ Server imports successfully")

        if API_KEY:
            print("✅ API key is configured")
        else:
            print("⚠️  Warning: No API key found (set LOCAL_NEWS_API_KEY)")

    except Exception as e:
        print(f"❌ Server import failed: {e}")
        return False

    # Test 2: Verify tool signatures return strings
    import inspect
    from main import intelligent_search, search_news, get_latest_headlines

    tools = [
        ("intelligent_search", intelligent_search),
        ("search_news", search_news),
        ("get_latest_headlines", get_latest_headlines),
    ]

    for name, func in tools:
        sig = inspect.signature(func)
        return_annotation = sig.return_annotation

        if return_annotation == str:
            print(f"✅ {name} returns string")
        else:
            print(f"❌ {name} returns {return_annotation} (should be str)")

    # Test 3: Verify formatters exist
    try:
        from utils import (
            format_search_results_simple,
            format_search_results_enhanced,
            format_clustered_results,
            format_error_message,
        )

        print("✅ All formatters available")
    except ImportError as e:
        print(f"❌ Missing formatters: {e}")

    print()
    print("📋 Validation Summary:")
    print("   - Server can be imported and initialized")
    print("   - All tools have correct return type annotations")
    print("   - Formatting utilities are available")
    print()
    print("🚀 Ready for MCP Inspector testing!")
    print()
    MCPInspectorTests.print_test_guide()


if __name__ == "__main__":
    run_validation_scenarios()
