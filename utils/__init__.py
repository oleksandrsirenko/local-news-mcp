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
    format_error_message,
)

from .clustering import (
    fetch_all_clustered_pages,
    extract_cluster_representatives,
    get_cluster_analysis,
)

__all__ = [
    # Formatters
    "format_article_simple",
    "format_article_enhanced",
    "format_search_results_simple",
    "format_search_results_enhanced",
    "format_clustered_results",
    "format_error_message",
    # Clustering
    "fetch_all_clustered_pages",
    "extract_cluster_representatives",
    "get_cluster_analysis",
]

__version__ = "0.1.1"
