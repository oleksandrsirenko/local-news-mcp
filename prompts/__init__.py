"""Prompt modules for Local News MCP server.

This module provides prompt creators for query enhancement and analysis functionality.
All prompt creators return lists of Message objects compatible with MCP prompts.
"""

from .query_enhancement import (
    create_enhancement_prompt,
    create_workflow_prompt,
    create_query_refinement_prompt,
)

from .analysis import (
    create_intent_analysis_prompt,
    create_domain_analysis_prompt,
    create_competitive_analysis_prompt,
)

__all__ = [
    # Query Enhancement
    "create_enhancement_prompt",
    "create_workflow_prompt",
    "create_query_refinement_prompt",
    # Analysis & Intent
    "create_intent_analysis_prompt",
    "create_domain_analysis_prompt",
    "create_competitive_analysis_prompt",
]

__version__ = "0.2.0"
