"""Simplified clustering utilities with pagination for Local News MCP server.

This module always uses clustering with pagination to ensure comprehensive
results for MCP clients. Keeps it simple - just fetch data and return it.
"""

from typing import Dict, List, Any, Tuple
import math
import logging

logger = logging.getLogger(__name__)


async def fetch_all_clustered_pages(
    api_request_func, base_payload: dict, max_pages: int = 5
) -> Dict[str, Any]:
    """Fetch multiple pages of clustered results for comprehensive coverage.

    Args:
        api_request_func: Async function to make API requests
        base_payload: Base request payload
        max_pages: Maximum number of pages to fetch (default: 5)

    Returns:
        Combined clusters data with pagination info
    """
    all_clusters = {}
    total_articles_processed = 0
    first_page_metadata = None

    for page_num in range(1, max_pages + 1):
        # Create payload for this page
        page_payload = {**base_payload, "page": page_num}

        # Make API request
        page_data = await api_request_func("/api/search", page_payload)

        if not page_data or not page_data.get("clusters"):
            break

        # Store metadata from first page
        if page_num == 1:
            first_page_metadata = {
                "status": page_data.get("status"),
                "total_hits": page_data.get("total_hits", 0),
                "total_pages": page_data.get("total_pages", 1),
                "page_size": page_data.get("page_size", 1000),
            }

            # If only one page, just return it
            if first_page_metadata["total_pages"] <= 1:
                return page_data

        # Process clusters from this page
        page_clusters = page_data.get("clusters", {})
        articles_this_page = 0

        for cluster_id, cluster_data in page_clusters.items():
            articles_in_cluster = len(cluster_data.get("articles", []))
            articles_this_page += articles_in_cluster

            if cluster_id in all_clusters:
                # Merge articles from same cluster across pages
                existing_articles = all_clusters[cluster_id]["articles"]
                new_articles = cluster_data["articles"]

                # Deduplicate by URL
                seen_urls = {article.get("link", "") for article in existing_articles}
                unique_new_articles = [
                    article
                    for article in new_articles
                    if article.get("link", "") not in seen_urls
                ]

                all_clusters[cluster_id]["articles"].extend(unique_new_articles)
            else:
                # New cluster
                all_clusters[cluster_id] = cluster_data

        total_articles_processed += articles_this_page

        # Stop if we've reached the last page
        if page_num >= first_page_metadata.get("total_pages", 1):
            break

    # Combine results
    combined_data = {
        "status": first_page_metadata["status"] if first_page_metadata else "ok",
        "total_hits": (
            first_page_metadata["total_hits"]
            if first_page_metadata
            else total_articles_processed
        ),
        "total_pages": first_page_metadata["total_pages"] if first_page_metadata else 1,
        "page_size": first_page_metadata["page_size"] if first_page_metadata else 1000,
        "clusters_count": len(all_clusters),
        "clusters": all_clusters,
        "pagination_info": {
            "pages_fetched": page_num,
            "total_articles_processed": total_articles_processed,
            "unique_clusters": len(all_clusters),
        },
    }

    return combined_data


def extract_cluster_representatives(
    combined_data: dict, max_representatives: int = 50
) -> List[Dict[str, Any]]:
    """Extract top cluster representatives for MCP client.

    Args:
        combined_data: Combined clusters data
        max_representatives: Maximum number of representatives to return

    Returns:
        List of cluster representatives with full article data
    """
    if not combined_data.get("clusters"):
        return []

    representatives = []
    clusters = combined_data["clusters"]

    # Calculate quality metrics for each cluster
    cluster_metrics = []

    for cluster_id, cluster_data in clusters.items():
        articles = cluster_data.get("articles", [])
        if not articles:
            continue

        cluster_size = len(articles)
        top_article = max(articles, key=lambda x: x.get("score", 0))
        avg_score = sum(article.get("score", 0) for article in articles) / cluster_size

        # Simple quality score: article quality + cluster size bonus
        quality_score = (
            top_article.get("score", 0) * 0.7  # Article quality (70%)
            + math.log(cluster_size + 1) * 0.3  # Cluster size bonus (30%)
        )

        cluster_metrics.append(
            {
                "cluster_id": cluster_id,
                "cluster_size": cluster_size,
                "quality_score": quality_score,
                "top_article": top_article.copy(),
                "avg_score": avg_score,
            }
        )

    # Sort by quality score (best first)
    cluster_metrics.sort(key=lambda x: x["quality_score"], reverse=True)

    # Extract representatives
    for i, cluster_info in enumerate(cluster_metrics[:max_representatives]):
        article = cluster_info["top_article"].copy()

        # Add cluster context to article
        article["cluster_metadata"] = {
            "cluster_id": cluster_info["cluster_id"],
            "cluster_rank": i + 1,
            "cluster_size": cluster_info["cluster_size"],
            "cluster_quality_score": cluster_info["quality_score"],
        }

        representatives.append(
            {
                "cluster_id": cluster_info["cluster_id"],
                "cluster_rank": i + 1,
                "cluster_size": cluster_info["cluster_size"],
                "cluster_score": cluster_info["quality_score"],
                "article": article,
            }
        )

    return representatives


def get_cluster_analysis(combined_data: dict) -> Dict[str, Any]:
    """Get basic cluster analysis for MCP client.

    Args:
        combined_data: Combined clusters data

    Returns:
        Basic cluster statistics
    """
    clusters = combined_data.get("clusters", {})

    if not clusters:
        return {"total_clusters": 0}

    cluster_sizes = [
        len(cluster_data.get("articles", [])) for cluster_data in clusters.values()
    ]
    cluster_sizes.sort(reverse=True)
    total_articles = sum(cluster_sizes)

    return {
        "total_clusters": len(clusters),
        "total_articles": total_articles,
        "largest_cluster": max(cluster_sizes) if cluster_sizes else 0,
        "average_cluster_size": (
            sum(cluster_sizes) / len(cluster_sizes) if cluster_sizes else 0
        ),
        "clusters_with_10_plus": sum(1 for size in cluster_sizes if size >= 10),
        "clusters_with_50_plus": sum(1 for size in cluster_sizes if size >= 50),
        "coverage_percentage": (
            (total_articles / combined_data.get("total_hits", 1)) * 100
            if combined_data.get("total_hits")
            else 0
        ),
    }
