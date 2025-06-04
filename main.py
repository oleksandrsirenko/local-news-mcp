from typing import Any, List, Optional
import httpx
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("local-news")

# Constants
LOCAL_NEWS_API_BASE = "https://local-news.newscatcherapi.com"
API_KEY = os.getenv("LOCAL_NEWS_API_KEY")


async def make_news_request(endpoint: str, payload: dict) -> dict[str, Any] | None:
    """Make a request to the Local News API."""
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
        except Exception:
            return None


def format_article(article: dict) -> str:
    """Format an article into a readable string."""
    # Use NLP summary if available, fall back to description
    summary = article.get("nlp", {}).get("summary") or article.get(
        "description", "No description available"
    )

    # Format locations if available
    locations_info = ""
    if article.get("locations"):
        location_strings = [
            f"{loc.get('name', 'Unknown')}" for loc in article.get("locations", [])
        ]
        if location_strings:
            locations_info = f"Locations: {'; '.join(location_strings)}\n"

    return f"""
    Title: {article.get('title', 'No title')}
    Source: {article.get('domain_url', 'Unknown source')}
    Published: {article.get('published_date', 'Unknown date')}
    {locations_info}Summary: {summary}
    URL: {article.get('link', 'No link')}
    """


@mcp.tool()
async def search_news(
    q: str,
    locations: List[str] = None,
    from_: str = "7 days ago",
    theme: Optional[str] = None,
    page_size: int = 10,
) -> str:
    """Search for news articles based on keywords and locations.

    Args:
        q: Advanced search query with support for boolean operators and special syntax.
           - Use double quotes with backslash escaping for exact phrases: \"artificial intelligence\"
           - Boolean operators: AND, OR, NOT (e.g., Tesla AND \"Elon Musk\")
           - Wildcards: Use * for any string (e.g., elect* finds election, electoral)
           - Combine with parentheses: (Apple OR Google) AND smartphone
           - Exclude terms with NOT: Tesla NOT SpaceX
           - Default operator between words is AND: "artificial intelligence" is the same as "artificial AND intelligence"
        locations: List of locations in "City, State" or "State" format (e.g. ["San Francisco, California", "New York City, New York"], ["California", "Texas"]).
        from_: Start date for search (e.g. "7 days ago" or "2023-01-01"). Limited to 30 days maximum.
        theme: Filter by theme (Business, Economics, Entertainment, Finance, Health, Politics, Science, Sports, Tech, Crime, Lifestyle, Travel, General)
        page_size: Number of articles to return (1-1000, default: 10)
    """
    # Build the search payload
    payload = {"q": q, "from_": from_, "page_size": page_size}
    if locations:
        payload["locations"] = locations
    if theme:
        payload["theme"] = theme

    data = await make_news_request("/api/search", payload)

    if not data or "articles" not in data or not data["articles"]:
        return f"No articles found matching '{q}'"

    articles = data["articles"]
    results = [format_article(article) for article in articles]
    total_hits = data.get("total_hits", 0)

    return (
        f"Found {total_hits} articles matching '{q}'. Showing top {len(articles)}:\n\n"
        + "\n---\n".join(results)
    )


@mcp.tool()
async def get_latest_headlines(
    locations: List[str] = None,
    when: str = "7d",
    theme: Optional[str] = None,
    page_size: int = 10,
) -> str:
    """Get the latest news headlines for specific locations.

    Args:
        locations: List of locations in "City, State" or "State" format (e.g. ["San Francisco, California", "New York City, New York"], ["California", "Texas"]).
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
        return f"No headlines found for {', '.join(locations)}"

    articles = data["articles"]
    results = [format_article(article) for article in articles]
    total_hits = data.get("total_hits", 0)

    return (
        f"Latest headlines for {', '.join(locations)} (found {total_hits}, showing {len(articles)}):\n\n"
        + "\n---\n".join(results)
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
