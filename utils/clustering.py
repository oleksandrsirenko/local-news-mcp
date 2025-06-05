"""Clustering utilities for Local News MCP server.

This module provides utilities for processing clustered search results,
extracting cluster representatives, and determining when to use clustering.
"""

from typing import Dict, List, Any, Optional


def should_use_clustering(
    query: str, page_size: int, estimated_results: Optional[int] = None
) -> bool:
    """Determine if clustering should be enabled based on query characteristics.

    Args:
        query: The search query
        page_size: Number of results requested
        estimated_results: Estimated number of results (if known)

    Returns:
        Boolean indicating whether clustering should be used
    """
    # Always use clustering for larger result sets
    if page_size >= 50:
        return True

    # Use clustering for broad, general queries that might have duplicates
    broad_terms = [
        "layoffs",
        "merger",
        "acquisition",
        "funding",
        "investment",
        "policy",
        "regulation",
        "crisis",
        "shortage",
        "disruption",
        "fire",
        "flood",
        "earthquake",
        "storm",
        "accident",
        "breakthrough",
        "launch",
        "partnership",
        "deal",
    ]

    query_lower = query.lower()
    for term in broad_terms:
        if term in query_lower:
            return True

    # Use clustering if query is short and likely to return many similar results
    # Count actual search terms (excluding operators)
    import re

    search_terms = re.findall(r"\b[a-zA-Z]+\b", query)
    meaningful_terms = [
        term
        for term in search_terms
        if term.lower() not in ["and", "or", "not", "near"]
    ]

    if len(meaningful_terms) <= 3:
        return True

    return False


def extract_cluster_representatives(data: dict) -> List[Dict[str, Any]]:
    """Extract the top representative article from each cluster.

    Args:
        data: API response data with clustering information

    Returns:
        List of cluster representatives with metadata
    """
    if not data.get("clusters"):
        return []

    representatives = []
    clusters = data["clusters"]

    # Sort clusters by the score of their top article (descending)
    sorted_cluster_ids = sorted(
        clusters.keys(),
        key=lambda cluster_id: (
            max(article.get("score", 0) for article in clusters[cluster_id]["articles"])
            if clusters[cluster_id]["articles"]
            else 0
        ),
        reverse=True,
    )

    for cluster_id in sorted_cluster_ids:
        cluster_data = clusters[cluster_id]
        articles = cluster_data["articles"]

        if not articles:
            continue

        # Get the top article from this cluster (highest score)
        top_article = max(articles, key=lambda x: x.get("score", 0))

        # Add cluster metadata to the article
        top_article["cluster_id"] = cluster_id
        top_article["cluster_rank"] = 1  # This is the top article in its cluster

        representatives.append(
            {
                "cluster_id": cluster_id,
                "article": top_article,
                "cluster_size": len(articles),
                "cluster_score": top_article.get("score", 0),
            }
        )

    # Sort representatives by cluster score (descending)
    representatives.sort(key=lambda x: x["cluster_score"], reverse=True)

    return representatives


def format_cluster_summary(data: dict) -> str:
    """Generate a summary of clustering information.

    Args:
        data: API response data with clustering information

    Returns:
        Formatted string with clustering summary
    """
    if not data.get("clusters"):
        return "No clustering information available."

    total_hits = data.get("total_hits", 0)
    clusters_count = data.get("clusters_count", 0)
    clusters = data.get("clusters", {})

    # Calculate cluster size distribution
    cluster_sizes = [len(cluster["articles"]) for cluster in clusters.values()]

    if cluster_sizes:
        avg_cluster_size = sum(cluster_sizes) / len(cluster_sizes)
        max_cluster_size = max(cluster_sizes)
        min_cluster_size = min(cluster_sizes)
    else:
        avg_cluster_size = max_cluster_size = min_cluster_size = 0

    summary = f"""Clustering Summary:
Total Articles: {total_hits:,}
Total Clusters: {clusters_count}
Average Cluster Size: {avg_cluster_size:.1f} articles
Largest Cluster: {max_cluster_size} articles
Smallest Cluster: {min_cluster_size} articles

This means the API found {clusters_count} distinct stories/events,
with an average of {avg_cluster_size:.1f} articles covering each story."""

    return summary


def get_cluster_themes_distribution(data: dict) -> Dict[str, int]:
    """Analyze theme distribution across clusters.

    Args:
        data: API response data with clustering information

    Returns:
        Dictionary mapping themes to cluster counts
    """
    if not data.get("clusters"):
        return {}

    theme_counts = {}
    clusters = data["clusters"]

    for cluster_data in clusters.values():
        articles = cluster_data["articles"]
        if not articles:
            continue

        # Get themes from the top article in the cluster
        top_article = max(articles, key=lambda x: x.get("score", 0))
        themes = top_article.get("nlp", {}).get("theme", [])

        for theme in themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

    return theme_counts


def get_cluster_location_distribution(data: dict) -> Dict[str, int]:
    """Analyze location distribution across clusters.

    Args:
        data: API response data with clustering information

    Returns:
        Dictionary mapping locations to cluster counts
    """
    if not data.get("clusters"):
        return {}

    location_counts = {}
    clusters = data["clusters"]

    for cluster_data in clusters.values():
        articles = cluster_data["articles"]
        if not articles:
            continue

        # Get locations from the top article in the cluster
        top_article = max(articles, key=lambda x: x.get("score", 0))
        locations = top_article.get("locations", [])

        for location in locations:
            location_name = location.get("name", "Unknown")
            location_counts[location_name] = location_counts.get(location_name, 0) + 1

    return location_counts


def analyze_cluster_quality(data: dict) -> Dict[str, Any]:
    """Analyze the quality and characteristics of clustering results.

    Args:
        data: API response data with clustering information

    Returns:
        Dictionary with clustering quality metrics
    """
    if not data.get("clusters"):
        return {"error": "No clustering data available"}

    clusters = data["clusters"]
    total_articles = sum(len(cluster["articles"]) for cluster in clusters.values())
    cluster_count = len(clusters)

    # Calculate clustering efficiency
    if total_articles > 0:
        clustering_efficiency = cluster_count / total_articles
        diversity_score = min(
            1.0, cluster_count / 20
        )  # Normalize to 0-1, good if 20+ clusters
    else:
        clustering_efficiency = 0
        diversity_score = 0

    # Get size distribution
    cluster_sizes = [len(cluster["articles"]) for cluster in clusters.values()]
    avg_size = sum(cluster_sizes) / len(cluster_sizes) if cluster_sizes else 0

    # Theme and location diversity
    theme_distribution = get_cluster_themes_distribution(data)
    location_distribution = get_cluster_location_distribution(data)

    return {
        "total_articles": total_articles,
        "cluster_count": cluster_count,
        "average_cluster_size": avg_size,
        "clustering_efficiency": clustering_efficiency,
        "diversity_score": diversity_score,
        "theme_diversity": len(theme_distribution),
        "location_diversity": len(location_distribution),
        "top_themes": dict(
            sorted(theme_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
        ),
        "top_locations": dict(
            sorted(location_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
        ),
    }
