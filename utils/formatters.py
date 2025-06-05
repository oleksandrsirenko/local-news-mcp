"""Response formatting utilities for Local News MCP server.

This module provides different formatting approaches for search results,
including simple (original), enhanced, and clustered formatting.
"""

from typing import Dict, Any, Optional


def format_article_simple(article: dict) -> str:
    """Format article using the original simple approach."""
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

    return f"""Title: {article.get('title', 'No title')}
Source: {article.get('domain_url', 'Unknown source')}
Published: {article.get('published_date', 'Unknown date')}
{locations_info}Summary: {summary}
URL: {article.get('link', 'No link')}"""


def format_article_enhanced(article: dict) -> str:
    """Format article with enhanced metadata and clustering info."""
    # Use NLP summary if available, fall back to description
    summary = article.get("nlp", {}).get("summary") or article.get(
        "description", "No description available"
    )

    # Format locations with detection methods
    locations_info = ""
    if article.get("locations"):
        location_details = []
        for loc in article.get("locations", []):
            name = loc.get("name", "Unknown")
            methods = loc.get("detection_methods", [])
            if methods:
                location_details.append(f"{name} ({', '.join(methods)})")
            else:
                location_details.append(name)

        if location_details:
            locations_info = f"Locations: {'; '.join(location_details)}\n"

    # Add sentiment info if available
    sentiment_info = ""
    if article.get("nlp", {}).get("sentiment"):
        sentiment = article["nlp"]["sentiment"]
        title_sentiment = sentiment.get("title", 0)
        content_sentiment = sentiment.get("content", 0)

        def sentiment_label(score):
            if score > 0.1:
                return "positive"
            elif score < -0.1:
                return "negative"
            else:
                return "neutral"

        sentiment_info = f"Sentiment: {sentiment_label(title_sentiment)} title, {sentiment_label(content_sentiment)} content\n"

    # Add theme info if available
    theme_info = ""
    if article.get("nlp", {}).get("theme"):
        themes = article["nlp"]["theme"]
        if themes:
            theme_info = f"Themes: {', '.join(themes)}\n"

    # Add clustering info if available
    cluster_info = ""
    if article.get("cluster_id"):
        cluster_rank = article.get("cluster_rank", "Unknown")
        cluster_info = f"Cluster: #{article['cluster_id']} (rank {cluster_rank})\n"

    return f"""Title: {article.get('title', 'No title')}
Source: {article.get('domain_url', 'Unknown source')}
Published: {article.get('published_date', 'Unknown date')}
{locations_info}{sentiment_info}{theme_info}{cluster_info}Summary: {summary}
URL: {article.get('link', 'No link')}"""


def format_search_results_simple(data: dict, enhancement_info: dict = None) -> str:
    """Format results using the original simple approach (backwards compatibility)."""
    if not data or "articles" not in data or not data["articles"]:
        return "No articles found matching the search criteria."

    result = ""
    if enhancement_info:
        result += "=== QUERY ENHANCEMENT ===\n"
        result += f"Original: {enhancement_info.get('original', '')}\n"
        result += f"Enhanced: {enhancement_info.get('enhanced', '')}\n"
        if enhancement_info.get("rationale"):
            result += f"Rationale: {enhancement_info.get('rationale', '')}\n"
        result += "\n"

    articles = data["articles"]
    total_hits = data.get("total_hits", 0)

    result += f"=== SEARCH RESULTS ===\n"
    result += f"Found {total_hits:,} articles. Showing top {len(articles)}:\n\n"
    result += "\n---\n".join([format_article_simple(article) for article in articles])

    return result


def format_search_results_enhanced(data: dict, enhancement_info: dict = None) -> str:
    """Format results with enhanced transparency and metadata."""
    if not data or "articles" not in data or not data["articles"]:
        return "No articles found matching the search criteria."

    result = ""

    # Enhancement transparency section
    if enhancement_info:
        result += "╔══════════════════════════════════════════════════════════════════════════════╗\n"
        result += "║                            QUERY ENHANCEMENT                                 ║\n"
        result += "╚══════════════════════════════════════════════════════════════════════════════╝\n"
        result += f"Original Input: {enhancement_info.get('original', 'N/A')}\n"
        result += f"Enhanced Query: {enhancement_info.get('enhanced', 'N/A')}\n"

        if enhancement_info.get("suggested_locations"):
            result += f"Suggested Locations: {', '.join(enhancement_info.get('suggested_locations', []))}\n"

        if enhancement_info.get("suggested_theme"):
            result += f"Suggested Theme: {enhancement_info.get('suggested_theme')}\n"

        if enhancement_info.get("detection_methods"):
            result += f"Detection Methods: {', '.join(enhancement_info.get('detection_methods', []))}\n"

        if enhancement_info.get("rationale"):
            result += f"Enhancement Rationale: {enhancement_info.get('rationale')}\n"

        result += "\n"

    # Results summary section
    articles = data["articles"]
    total_hits = data.get("total_hits", 0)
    page = data.get("page", 1)
    total_pages = data.get("total_pages", 1)

    result += "╔══════════════════════════════════════════════════════════════════════════════╗\n"
    result += "║                              SEARCH RESULTS                                  ║\n"
    result += "╚══════════════════════════════════════════════════════════════════════════════╝\n"
    result += f"Found: {total_hits:,} total articles\n"
    result += f"Showing: {len(articles)} articles (page {page} of {total_pages})\n"

    # Add search metadata if available
    if data.get("user_input"):
        search_params = data["user_input"]
        result += f"Query: {search_params.get('q', 'N/A')}\n"
        if search_params.get("locations"):
            result += f"Locations: {', '.join(search_params['locations'])}\n"
        if search_params.get("theme"):
            result += f"Theme Filter: {search_params['theme']}\n"
        if search_params.get("from_"):
            result += f"Time Range: {search_params['from_']}\n"

    result += "\n"

    # Articles section
    result += "╔══════════════════════════════════════════════════════════════════════════════╗\n"
    result += "║                                 ARTICLES                                     ║\n"
    result += "╚══════════════════════════════════════════════════════════════════════════════╝\n\n"

    # Format each article with enhanced display
    formatted_articles = []
    for i, article in enumerate(articles, 1):
        article_header = f"[{i}/{len(articles)}] ──────────────────────────────────────────────────────────────────"
        formatted_article = format_article_enhanced(article)
        formatted_articles.append(f"{article_header}\n{formatted_article}")

    result += "\n\n".join(formatted_articles)

    # Add footer with tips
    result += "\n\n" + "─" * 80 + "\n"
    result += "💡 Tips: Use 'enhance-query' prompt for better results | Check location detection methods for confidence\n"

    return result


def format_clustered_results(
    data: dict, cluster_representatives: list, enhancement_info: dict = None
) -> str:
    """Format clustered results showing one representative article per cluster."""
    if not data or not cluster_representatives:
        return "No clustered articles found matching the search criteria."

    result = ""

    # Enhancement transparency section
    if enhancement_info:
        result += "╔══════════════════════════════════════════════════════════════════════════════╗\n"
        result += "║                            QUERY ENHANCEMENT                                 ║\n"
        result += "╚══════════════════════════════════════════════════════════════════════════════╝\n"
        result += f"Original Input: {enhancement_info.get('original', 'N/A')}\n"
        result += f"Enhanced Query: {enhancement_info.get('enhanced', 'N/A')}\n"

        if enhancement_info.get("rationale"):
            result += f"Enhancement Rationale: {enhancement_info.get('rationale')}\n"

        result += "\n"

    # Clustering summary section
    total_hits = data.get("total_hits", 0)
    clusters_count = data.get("clusters_count", 0)

    result += "╔══════════════════════════════════════════════════════════════════════════════╗\n"
    result += "║                           CLUSTERED RESULTS                                  ║\n"
    result += "╚══════════════════════════════════════════════════════════════════════════════╝\n"
    result += f"Found: {total_hits:,} total articles across {clusters_count} clusters\n"
    result += f"Showing: Top article from {len(cluster_representatives)} clusters (diverse stories)\n"
    result += (
        f"Clustering: Enabled to reduce duplicates and show varied perspectives\n\n"
    )

    # Add search metadata if available
    if data.get("user_input"):
        search_params = data["user_input"]
        result += f"Query: {search_params.get('q', 'N/A')}\n"
        if search_params.get("locations"):
            result += f"Locations: {', '.join(search_params['locations'])}\n"
        if search_params.get("theme"):
            result += f"Theme Filter: {search_params['theme']}\n"
        if search_params.get("from_"):
            result += f"Time Range: {search_params['from_']}\n"

    result += "\n"

    # Cluster representatives section
    result += "╔══════════════════════════════════════════════════════════════════════════════╗\n"
    result += "║                          CLUSTER REPRESENTATIVES                             ║\n"
    result += "╚══════════════════════════════════════════════════════════════════════════════╝\n\n"

    # Format each cluster representative
    formatted_articles = []
    for i, cluster_info in enumerate(cluster_representatives, 1):
        cluster_id = cluster_info["cluster_id"]
        article = cluster_info["article"]
        cluster_size = cluster_info["cluster_size"]

        article_header = f"[Cluster {i}/{len(cluster_representatives)}] ID: {cluster_id} | Size: {cluster_size} articles"
        article_header += "\n" + "─" * 80
        formatted_article = format_article_enhanced(article)
        formatted_articles.append(f"{article_header}\n{formatted_article}")

    result += "\n\n".join(formatted_articles)

    # Add footer with clustering tips
    result += "\n\n" + "─" * 80 + "\n"
    result += "🔗 Clustering enabled: Each result represents a different story/event\n"
    result += "💡 Tips: Use 'enhance-query' prompt for better results | Clustering reduces duplicate coverage\n"

    return result


def format_error_message(
    error_type: str, error_details: str, suggestions: list = None
) -> str:
    """Format error messages with helpful suggestions."""
    result = "╔══════════════════════════════════════════════════════════════════════════════╗\n"
    result += "║                                  ERROR                                       ║\n"
    result += "╚══════════════════════════════════════════════════════════════════════════════╝\n"

    result += f"Error Type: {error_type}\n"
    result += f"Details: {error_details}\n\n"

    if suggestions:
        result += "Suggestions:\n"
        for suggestion in suggestions:
            result += f"  • {suggestion}\n"
        result += "\n"

    result += "💡 Use 'guide://workflow' resource for usage help\n"
    result += "─" * 80

    return result
