from typing import Any, List, Optional
import httpx
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Import prompt creators
from prompts import (
    create_enhancement_prompt,
    create_workflow_prompt,
    create_intent_analysis_prompt,
    create_domain_analysis_prompt,
    create_competitive_analysis_prompt,
)

# Import formatting utilities
from utils import format_search_results_simple

# Import clustering utilities
from utils.clustering import (
    fetch_all_clustered_pages,
    extract_cluster_representatives,
    get_cluster_analysis,
)

load_dotenv()
mcp = FastMCP("local-news")

# Constants
LOCAL_NEWS_API_BASE = "https://local-news.newscatcherapi.com"
API_KEY = os.getenv("LOCAL_NEWS_API_KEY")
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


# Load query syntax guide once at startup
def load_query_syntax_guide() -> str:
    """Load the query syntax markdown guide."""
    try:
        with open(KNOWLEDGE_DIR / "query_syntax.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading query syntax guide: {e}")
        return "Query syntax guide not available."


QUERY_SYNTAX_GUIDE = load_query_syntax_guide()


# === RESOURCES ===
@mcp.resource("knowledge://query-syntax")
def get_query_syntax_guide() -> str:
    """Advanced query construction guide for News API v3."""
    return QUERY_SYNTAX_GUIDE


@mcp.resource("guide://workflow")
def get_workflow_guide() -> str:
    """Complete workflow guide for using Local News MCP effectively."""
    try:
        with open(KNOWLEDGE_DIR / "workflow_guide.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading workflow guide: {e}")
        return """
            # Local News MCP Workflow Guide

            ## Basic Usage
            1. Use 'enhance-query' prompt with simple input
            2. Use 'intelligent_search' tool with enhanced parameters
            3. Use 'search_news' for direct queries

            See documentation for complete guide.
            """


# === PROMPTS ===
@mcp.prompt("enhance-query")
def enhance_query_prompt(
    user_input: str, domain_context: str = "", location_focus: str = ""
) -> List[base.Message]:
    """Transform simple user input into sophisticated news search query."""
    return create_enhancement_prompt(
        user_input=user_input,
        domain_context=domain_context,
        location_focus=location_focus,
        query_syntax_guide=QUERY_SYNTAX_GUIDE,
    )


@mcp.prompt("analyze-search-intent")
def analyze_intent_prompt(user_input: str) -> List[base.Message]:
    """Analyze user search intent for comprehensive understanding."""
    return create_intent_analysis_prompt(user_input)


@mcp.prompt("workflow-guidance")
def workflow_guidance_prompt(complexity: str = "standard") -> List[base.Message]:
    """Get workflow recommendations for different search complexities."""
    return create_workflow_prompt(complexity)


@mcp.prompt("domain-expertise")
def domain_expertise_prompt(
    domain: str, specific_context: str = ""
) -> List[base.Message]:
    """Get domain-specific expertise for enhanced searches."""
    return create_domain_analysis_prompt(domain, specific_context)


@mcp.prompt("competitive-analysis")
def competitive_analysis_prompt(
    companies: List[str], analysis_focus: str = "general"
) -> List[base.Message]:
    """Design competitive intelligence monitoring strategies."""
    return create_competitive_analysis_prompt(companies, analysis_focus)


# === API CLIENT FUNCTIONS ===
async def make_news_request(endpoint: str, payload: dict) -> dict[str, Any] | None:
    """Make request to Local News API with enhanced error handling."""
    if not API_KEY:
        print("Error: LOCAL_NEWS_API_KEY not found in environment variables")
        return None

    headers = {
        "x-api-token": API_KEY,
        "Content-Type": "application/json",
    }
    url = f"{LOCAL_NEWS_API_BASE}{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url, json=payload, headers=headers, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            print(f"Request timeout for {endpoint}")
            return None
        except httpx.HTTPStatusError as e:
            print(
                f"HTTP error {e.response.status_code} for {endpoint}: {e.response.text}"
            )
            return None
        except Exception as e:
            print(f"Unexpected error for {endpoint}: {e}")
            return None


# === TOOLS ===
@mcp.tool()
async def intelligent_search(
    enhanced_query: str,
    locations: List[str] = None,
    theme: Optional[str] = None,
    detection_methods: List[str] = None,
    from_: str = "7d",
    max_clusters: int = 50,
    max_pages: int = 8,
    page_size: int = 1000,
    clustering: bool = True,
    original_query: str = "",
) -> dict:
    """Execute search with configurable clustering and pagination.

    Args:
        enhanced_query: Advanced search query with boolean operators from enhancement prompt.
                       Should include sophisticated syntax like exact phrases in quotes,
                       boolean operators (AND, OR, NOT), and domain-specific terminology.
        locations: List of locations in "City, State" or "State" format (e.g. ["San Francisco, California", "New York City, New York"], ["California", "Texas"]).
        theme: Filter by theme (Business, Economics, Entertainment, Finance, Health, Politics, Science, Sports, Tech, Crime, Lifestyle, Travel, General)
        detection_methods: Location detection methods for filtering. Options: ["dedicated_source", "local_section", "standard_format", "proximity_mention", "ai_extracted", "regional_source"]
        from_: Start date for search (e.g. "30 days ago", "7d", or "2023-01-01"). Limited to 30 days maximum.
        max_clusters: Maximum number of cluster representatives to return (1-100).
        max_pages: Maximum pages to fetch for pagination (1-10).
        page_size: Articles per API page (1-1000, default: 1000 for best clustering).
        clustering: Enable clustering (default: True for diverse results).
        original_query: Original user input before enhancement.

    Returns:
        Dict with structured search results for MCP client analysis.
    """

    # Build search payload with configurable parameters
    payload = {
        "q": enhanced_query,
        "from_": from_,
        "page_size": page_size,
        "clustering": clustering,
    }

    if locations:
        payload["locations"] = locations
    if theme:
        payload["theme"] = theme
    if detection_methods:
        payload["detection_methods"] = detection_methods

    # Fetch results - handle both clustered and non-clustered
    try:
        if clustering:
            # Use pagination for clustered results
            combined_data = await fetch_all_clustered_pages(
                make_news_request, payload, max_pages=max_pages
            )
        else:
            # Single request for non-clustered results
            combined_data = await make_news_request("/api/search", payload)

    except Exception as e:
        return {
            "success": False,
            "error": f"Search request failed: {str(e)}",
            "query_info": {
                "original_query": original_query,
                "enhanced_query": enhanced_query,
                "clustering_enabled": clustering,
            },
        }

    if not combined_data:
        return {
            "success": False,
            "error": "No results found",
            "query_info": {
                "original_query": original_query,
                "enhanced_query": enhanced_query,
                "clustering_enabled": clustering,
            },
        }

    # Process results based on clustering mode
    if clustering and combined_data.get("clusters"):
        # Clustered results processing
        cluster_representatives = extract_cluster_representatives(
            combined_data, max_representatives=max_clusters
        )
        cluster_analysis = get_cluster_analysis(combined_data)

        return {
            "success": True,
            "search_type": "clustered",
            "query_info": {
                "original_query": original_query,
                "enhanced_query": enhanced_query,
                "clustering_enabled": True,
            },
            "results": {
                "total_hits": combined_data.get("total_hits", 0),
                "total_clusters": len(combined_data.get("clusters", {})),
                "clusters_returned": len(cluster_representatives),
                "articles_processed": combined_data.get("pagination_info", {}).get(
                    "total_articles_processed", 0
                ),
                "coverage_percentage": cluster_analysis.get("coverage_percentage", 0),
                "cluster_representatives": cluster_representatives,
            },
            "clustering_analysis": cluster_analysis,
            "pagination_info": combined_data.get("pagination_info", {}),
            "metadata": {
                "search_params": {
                    "locations": locations,
                    "theme": theme,
                    "detection_methods": detection_methods,
                    "from": from_,
                    "page_size": page_size,
                    "max_pages_used": max_pages,
                },
                "pages_fetched": combined_data.get("pagination_info", {}).get(
                    "pages_fetched", 1
                ),
                "total_pages_available": combined_data.get("total_pages", 1),
            },
        }
    else:
        # Non-clustered results processing
        articles = combined_data.get("articles", [])

        return {
            "success": True,
            "search_type": "standard",
            "query_info": {
                "original_query": original_query,
                "enhanced_query": enhanced_query,
                "clustering_enabled": False,
            },
            "results": {
                "total_hits": combined_data.get("total_hits", 0),
                "articles_returned": len(articles),
                "articles": articles[:max_clusters],  # Limit articles if needed
            },
            "metadata": {
                "search_params": {
                    "locations": locations,
                    "theme": theme,
                    "detection_methods": detection_methods,
                    "from": from_,
                    "page_size": page_size,
                },
                "page": combined_data.get("page", 1),
                "total_pages": combined_data.get("total_pages", 1),
            },
        }


@mcp.tool()
async def search_news(
    q: str,
    locations: List[str] = None,
    from_: str = "7 days ago",
    theme: Optional[str] = None,
    page_size: int = 10,
) -> str:
    """Search for news articles based on keywords and locations.

    Direct search tool for users who want to provide their own queries without enhancement.
    For better results with simple input, use the 'enhance-query' prompt first.
    Uses simple formatting for backwards compatibility.

    Args:
        q: Advanced search query with support for boolean operators and special syntax.
           - Use double quotes with backslash escaping for exact phrases: \"artificial intelligence\"
           - Boolean operators: AND, OR, NOT (e.g., Tesla AND \"Elon Musk\")
           - Wildcards: Use * for any string (e.g., elect* finds election, electoral)
           - Combine with parentheses: (Apple OR Google) AND smartphone
           - Exclude terms with NOT: Tesla NOT SpaceX
        locations: List of locations in "City, State" or "State" format
        from_: Start date for search (e.g. "7 days ago" or "2023-01-01"). Limited to 30 days maximum.
        theme: Filter by theme (Business, Economics, Entertainment, Finance, Health, Politics, Science, Sports, Tech, Crime, Lifestyle, Travel, General)
        page_size: Number of articles to return (1-1000, default: 10)
    """
    payload = {"q": q, "from_": from_, "page_size": page_size}
    if locations:
        payload["locations"] = locations
    if theme:
        payload["theme"] = theme

    data = await make_news_request("/api/search", payload)
    return format_search_results_simple(data)


@mcp.tool()
async def get_latest_headlines(
    locations: List[str] = None,
    when: str = "7d",
    theme: Optional[str] = None,
    page_size: int = 10,
) -> str:
    """Get the latest news headlines for specific locations.

    Args:
        locations: List of locations in "City, State" or "State" format
        when: Time period (e.g. "7d" for 7 days, "24h" for 24 hours). Maximum 30d.
        theme: Filter by theme (Business, Economics, Entertainment, Finance, Health, Politics, Science, Sports, Tech, Crime, Lifestyle, Travel, General)
        page_size: Number of articles to return (1-1000, default: 10)
    """
    payload = {
        "when": when,
        "page_size": page_size,
    }
    if locations:
        payload["locations"] = locations
    if theme:
        payload["theme"] = theme

    data = await make_news_request("/api/latest_headlines", payload)

    if not data or "articles" not in data or not data["articles"]:
        location_str = ", ".join(locations) if locations else "all locations"
        return f"No headlines found for {location_str}"

    return format_search_results_simple(data)


if __name__ == "__main__":
    mcp.run(transport="stdio")
