"""
Comprehensive tests for Local News MCP server tools.

These tests ensure that all tools return properly formatted strings
and handle various scenarios correctly.
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path
import sys

# Add the project root to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import (
    intelligent_search,
    search_news,
    get_latest_headlines,
    make_news_request,
)


class TestToolReturnTypes:
    """Test that all tools return properly formatted strings."""

    @pytest.mark.asyncio
    async def test_intelligent_search_returns_string(self):
        """Test that intelligent_search always returns a string."""
        # Mock the API response
        mock_response = {
            "status": "ok",
            "total_hits": 100,
            "clusters": {
                "cluster_1": {
                    "articles": [
                        {
                            "title": "Test Article",
                            "domain_url": "example.com",
                            "published_date": "2024-01-01",
                            "description": "Test description",
                            "link": "https://example.com/article",
                            "score": 0.9,
                            "locations": [{"name": "San Francisco, California"}],
                        }
                    ]
                }
            },
        }

        with patch("main.fetch_all_clustered_pages", return_value=mock_response):
            result = await intelligent_search(
                enhanced_query="tech AND layoffs",
                locations=["San Francisco, California"],
                original_query="tech layoffs",
            )

            # CRITICAL: Must return string
            assert isinstance(
                result, str
            ), f"intelligent_search returned {type(result)}, expected str"
            assert len(result) > 0, "Result string should not be empty"
            assert "SEARCH RESULTS" in result or "CLUSTERED RESULTS" in result

    @pytest.mark.asyncio
    async def test_search_news_returns_string(self):
        """Test that search_news always returns a string."""
        mock_response = {
            "articles": [
                {
                    "title": "Test Article",
                    "domain_url": "example.com",
                    "published_date": "2024-01-01",
                    "description": "Test description",
                    "link": "https://example.com/article",
                }
            ],
            "total_hits": 1,
        }

        with patch("main.make_news_request", return_value=mock_response):
            result = await search_news(
                q="test query", locations=["San Francisco, California"]
            )

            # CRITICAL: Must return string
            assert isinstance(
                result, str
            ), f"search_news returned {type(result)}, expected str"
            assert len(result) > 0, "Result string should not be empty"

    @pytest.mark.asyncio
    async def test_get_latest_headlines_returns_string(self):
        """Test that get_latest_headlines always returns a string."""
        mock_response = {
            "articles": [
                {
                    "title": "Latest News",
                    "domain_url": "news.com",
                    "published_date": "2024-01-01",
                    "description": "Latest news description",
                    "link": "https://news.com/latest",
                }
            ]
        }

        with patch("main.make_news_request", return_value=mock_response):
            result = await get_latest_headlines(locations=["Los Angeles, California"])

            # CRITICAL: Must return string
            assert isinstance(
                result, str
            ), f"get_latest_headlines returned {type(result)}, expected str"
            assert len(result) > 0, "Result string should not be empty"


class TestIntelligentSearchFormatting:
    """Test intelligent_search formatting in various scenarios."""

    @pytest.mark.asyncio
    async def test_clustered_results_formatting(self):
        """Test that clustered results are properly formatted."""
        mock_response = {
            "status": "ok",
            "total_hits": 500,
            "clusters_count": 25,
            "clusters": {
                "cluster_1": {
                    "articles": [
                        {
                            "title": "Tech Layoffs Hit San Francisco",
                            "domain_url": "techcrunch.com",
                            "published_date": "2024-01-01T10:00:00Z",
                            "description": "Major tech companies announce layoffs",
                            "link": "https://techcrunch.com/layoffs",
                            "score": 0.95,
                            "cluster_id": "cluster_1",
                            "cluster_rank": 1,
                            "locations": [
                                {
                                    "name": "San Francisco, California",
                                    "detection_methods": ["dedicated_source"],
                                }
                            ],
                            "nlp": {
                                "summary": "Tech companies reducing workforce",
                                "sentiment": {"title": -0.3, "content": -0.2},
                                "theme": ["Tech", "Business"],
                            },
                        }
                    ]
                }
            },
            "pagination_info": {
                "pages_fetched": 2,
                "total_articles_processed": 100,
                "unique_clusters": 25,
            },
        }

        with patch("main.fetch_all_clustered_pages", return_value=mock_response):
            result = await intelligent_search(
                enhanced_query='technology AND (layoffs OR "job cuts")',
                locations=["San Francisco, California"],
                theme="Tech",
                clustering=True,
                original_query="tech layoffs",
            )

            # Verify string format and content
            assert isinstance(result, str)
            assert "QUERY ENHANCEMENT" in result
            assert "CLUSTERED RESULTS" in result
            assert "Enhanced Query:" in result
            assert 'technology AND (layoffs OR "job cuts")' in result
            assert "San Francisco, California" in result
            assert "Tech Layoffs Hit San Francisco" in result

    @pytest.mark.asyncio
    async def test_non_clustered_results_formatting(self):
        """Test that non-clustered results are properly formatted."""
        mock_response = {
            "status": "ok",
            "total_hits": 50,
            "articles": [
                {
                    "title": "Housing Market Update",
                    "domain_url": "realestate.com",
                    "published_date": "2024-01-01T15:00:00Z",
                    "description": "Housing prices continue to rise",
                    "link": "https://realestate.com/update",
                    "locations": [{"name": "Los Angeles, California"}],
                }
            ],
        }

        with patch("main.make_news_request", return_value=mock_response):
            result = await intelligent_search(
                enhanced_query='"real estate" AND market',
                locations=["Los Angeles, California"],
                clustering=False,
                original_query="housing market",
            )

            # Verify string format and content
            assert isinstance(result, str)
            assert "QUERY ENHANCEMENT" in result
            assert "SEARCH RESULTS" in result
            assert "Enhanced Query:" in result
            assert "Housing Market Update" in result


class TestErrorHandling:
    """Test error handling returns properly formatted strings."""

    @pytest.mark.asyncio
    async def test_api_request_failure(self):
        """Test handling of API request failures."""
        with patch(
            "main.fetch_all_clustered_pages", side_effect=Exception("API Error")
        ):
            result = await intelligent_search(
                enhanced_query="test query", original_query="test"
            )

            # Should return formatted error string
            assert isinstance(result, str)
            assert "ERROR" in result
            assert "Search Request Failed" in result
            assert "API request failed" in result

    @pytest.mark.asyncio
    async def test_no_results_found(self):
        """Test handling when no results are returned."""
        with patch("main.fetch_all_clustered_pages", return_value=None):
            result = await intelligent_search(
                enhanced_query="nonexistent query", original_query="nothing"
            )

            # Should return formatted error string
            assert isinstance(result, str)
            assert "ERROR" in result
            assert "No Results Found" in result

    @pytest.mark.asyncio
    async def test_processing_failure(self):
        """Test handling of result processing failures."""
        # Mock response that will cause processing error
        mock_response = {
            "status": "ok",
            "clusters": {"invalid_cluster": "this will cause an error"},
        }

        with patch("main.fetch_all_clustered_pages", return_value=mock_response):
            result = await intelligent_search(
                enhanced_query="test query", clustering=True
            )

            # Should return formatted error string
            assert isinstance(result, str)
            assert "ERROR" in result
            assert "Result Processing Failed" in result


class TestMCPCompatibility:
    """Test MCP-specific compatibility requirements."""

    @pytest.mark.asyncio
    async def test_no_dict_returns(self):
        """Ensure no tool ever returns a dictionary (MCP incompatible)."""

        # Test intelligent_search
        with patch("main.fetch_all_clustered_pages", return_value={"articles": []}):
            result = await intelligent_search("test")
            assert not isinstance(
                result, dict
            ), "intelligent_search returned dict (MCP incompatible)"

        # Test search_news
        with patch("main.make_news_request", return_value={"articles": []}):
            result = await search_news("test")
            assert not isinstance(
                result, dict
            ), "search_news returned dict (MCP incompatible)"

        # Test get_latest_headlines
        with patch("main.make_news_request", return_value={"articles": []}):
            result = await get_latest_headlines()
            assert not isinstance(
                result, dict
            ), "get_latest_headlines returned dict (MCP incompatible)"

    @pytest.mark.asyncio
    async def test_non_empty_responses(self):
        """Ensure all tools return non-empty responses."""

        # Mock empty but valid API response
        empty_response = {"articles": [], "total_hits": 0}

        with patch("main.make_news_request", return_value=empty_response):
            result = await search_news("test")
            assert len(result.strip()) > 0, "search_news returned empty string"

        with patch("main.make_news_request", return_value=empty_response):
            result = await get_latest_headlines()
            assert len(result.strip()) > 0, "get_latest_headlines returned empty string"


class TestEnhancementInfo:
    """Test that enhancement information is properly included."""

    @pytest.mark.asyncio
    async def test_enhancement_transparency(self):
        """Test that original and enhanced queries are shown - FIXED VERSION."""
        mock_response = {
            "clusters": {
                "cluster_1": {
                    "articles": [
                        {"title": "Test", "link": "http://test.com", "score": 0.8}
                    ]
                }
            },
            "total_hits": 1,
        }

        with patch("main.fetch_all_clustered_pages", return_value=mock_response):
            result = await intelligent_search(
                enhanced_query="technology AND layoffs NOT sports",
                original_query="tech layoffs",
                locations=["San Francisco, California"],
                theme="Tech",
            )

            # Verify enhancement transparency - more flexible checks
            assert "tech layoffs" in result, "Should show original query"
            assert (
                "technology AND layoffs NOT sports" in result
            ), "Should show enhanced query"
            assert "San Francisco, California" in result, "Should include the location"
            assert "Tech" in result, "Should include the theme"

            # Check for the enhancement section
            assert (
                "QUERY ENHANCEMENT" in result or "Enhanced Query:" in result
            ), "Should have enhancement section"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
