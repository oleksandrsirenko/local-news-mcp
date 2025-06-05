"""Utilities for Local News MCP server.

This module provides utilities for response formatting, clustering,
and other processing functions.
"""

from .formatters import (
    format_article_simple,
    format_article_enhanced,
    format_search_results_simple,
    format_search_results_enhanced,
    format_clustered_results,
)

from .clustering import (
    extract_cluster_representatives,
    format_cluster_summary,
    should_use_clustering,
)

__all__ = [
    # Formatters
    "format_article_simple",
    "format_article_enhanced",
    "format_search_results_simple",
    "format_search_results_enhanced",
    "format_clustered_results",
    # Clustering
    "extract_cluster_representatives",
    "format_cluster_summary",
    "should_use_clustering",
]

__version__ = "0.1.0"
