"""Query enhancement prompts for Local News MCP server.

This module provides prompt creators for transforming simple user input
into sophisticated search queries with boolean operators and domain expertise.
"""

from typing import List, Optional
from mcp.server.fastmcp.prompts import base


def create_enhancement_prompt(
    user_input: str,
    domain_context: str = "",
    location_focus: str = "",
    query_syntax_guide: str = "",
) -> List[base.Message]:
    """Create comprehensive query enhancement prompt.

    Args:
        user_input: Simple user search input to enhance
        domain_context: Optional domain hint (business, tech, etc.)
        location_focus: Optional location focus hint
        query_syntax_guide: Query syntax reference from knowledge base

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = f"""You are an expert news search query optimizer specializing in local news discovery. Your task is to transform simple user input into sophisticated, precise search queries that leverage boolean operators and domain expertise.

QUERY SYNTAX REFERENCE:
{query_syntax_guide}

CORE ENHANCEMENT PRINCIPLES:

1. **Domain Expansion**: Identify the primary domain and expand with relevant terminology
   - Business: Include corporate, financial, commercial, enterprise terms
   - Technology: Include digital, innovation, startup, platform concepts
   - Politics: Include policy, governance, regulatory, legislative terms
   - Real Estate: Include property, housing, development, zoning terms
   - Healthcare: Include medical, hospital, pharmaceutical, public health terms

2. **Synonym Integration**: Use OR operators to capture concept variations
   - "layoffs OR \\"job cuts\\" OR downsizing OR restructuring OR \\"workforce reduction\\""
   - "funding OR investment OR capital OR financing OR \\"series A\\""
   - "regulation* OR policy OR legislation OR compliance"

3. **Contextual Specificity**: Add industry context with AND operators
   - "startup AND (funding OR investment) AND (tech* OR technolog*)"
   - "real estate AND (market OR prices OR development) AND local"
   - "hospital AND (merger OR acquisition OR expansion)"

4. **Noise Elimination**: Use NOT operators to exclude irrelevant content
   - "NOT (sports OR entertainment OR celebrity OR gossip)"
   - "NOT (vacation OR tourism OR recreation)" for business queries
   - "NOT (historical OR archive OR \\"years ago\\")" for recent news

5. **Exact Phrase Targeting**: Use escaped quotes for specific concepts
   - "\\"supply chain\\"", "\\"artificial intelligence\\"", "\\"venture capital\\""
   - "\\"public health\\"", "\\"real estate market\\"", "\\"tech layoffs\\""

6. **Wildcard Utilization**: Use asterisks for term variations
   - "regulat*" captures regulation, regulatory, regulator
   - "invest*" captures investment, investor, investing
   - "technolog*" captures technology, technological, technologies

7. **Geographic Intelligence**: 
   - Understand regional aliases (Bay Area → San Francisco, San Jose, etc.)
   - Consider industry hubs for relevant topics
   - Include state context when cities are mentioned
   - Use proximity for related geographic terms

8. **Boolean Logic Best Practices**:
   - Use parentheses for grouping: (term1 OR term2) AND (term3 OR term4)
   - Put most important terms first
   - Balance precision with recall
   - Avoid overly complex nested logic

OUTPUT REQUIREMENTS:
Provide a structured response with:
- Enhanced Query: [sophisticated boolean query with proper JSON escaping]
- Suggested Locations: [specific "City, State" locations if relevant]  
- Suggested Theme: [Business|Tech|Politics|Health|Sports|Finance|Crime|etc.]
- Detection Methods: [recommended detection methods array]
- Rationale: [brief explanation of enhancements made]

QUALITY STANDARDS:
- Query must be significantly more sophisticated than input
- Include 3-7 boolean operators for complex topics
- Balance precision with recall
- Prioritize recent, relevant local news discovery
- Ensure query would work across different news sources
- Properly escape quotes for JSON format"""

    user_message = f"""Transform this search input into an advanced local news query:

USER INPUT: "{user_input}"
DOMAIN CONTEXT: {domain_context or "Auto-detect from input"}
LOCATION FOCUS: {location_focus or "Auto-detect or suggest relevant locations"}

Create a sophisticated boolean search query optimized for local news discovery. Consider:
- What domain expertise is needed?
- What synonyms and related terms should be included?
- What noise should be excluded?
- What locations would be most relevant?
- What time sensitivity is implied?
- How can boolean logic improve precision?

Remember to properly escape quotes for JSON format in your enhanced query.

Provide your enhancement following the structured output format."""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_workflow_prompt(query_complexity: str = "standard") -> List[base.Message]:
    """Create workflow guidance prompt for different query complexities.

    Args:
        query_complexity: Level of complexity (simple, standard, complex)

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = """You are a Local News MCP workflow advisor. Guide users on the most effective approach for their search needs based on query complexity and desired outcomes."""

    workflow_guidance = {
        "simple": """For simple, direct searches:
1. Use 'search_news' tool directly with your query
2. Add specific locations if you have them
3. Use theme filters for broad categorization
4. Good for: Quick lookups, known entities, simple topics""",
        "standard": """For enhanced relevance (RECOMMENDED):
1. Use 'enhance-query' prompt with your input
2. Review the enhanced query and suggestions  
3. Use 'intelligent_search' tool with enhanced parameters
4. Iterate if results need refinement
5. Good for: Most searches, domain research, location-specific needs""",
        "complex": """For complex research and analysis:
1. Use 'analyze-search-intent' prompt to understand your needs
2. Use 'enhance-query' prompt with domain context
3. Execute multiple 'intelligent_search' calls with variations
4. Consider different time ranges and location scopes
5. Use 'get_latest_headlines' for breaking developments
6. Good for: Market research, competitive analysis, trend tracking""",
    }

    user_message = f"""Recommend the optimal workflow approach for {query_complexity} queries. 

Include:
- Step-by-step process
- When to use each tool/prompt
- Tips for better results
- Common pitfalls to avoid
- Expected outcomes

Focus on practical guidance that helps users get the most relevant results efficiently.

{workflow_guidance.get(query_complexity, workflow_guidance['standard'])}"""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_query_refinement_prompt(
    original_query: str, search_results_summary: dict, refinement_goal: str
) -> List[base.Message]:
    """Create prompt for refining queries based on results.

    Args:
        original_query: The original search query used
        search_results_summary: Summary of search results received
        refinement_goal: What the user wants to improve

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = """You are a query refinement specialist. Analyze search results and improve queries for better targeting based on user feedback and result quality."""

    total_hits = search_results_summary.get("total_hits", 0)
    articles_returned = search_results_summary.get("articles_count", 0)

    user_message = f"""Refine this query based on the results received:

ORIGINAL QUERY: "{original_query}"
REFINEMENT GOAL: {refinement_goal}
RESULTS SUMMARY: {articles_returned} articles returned, {total_hits} total hits available

ANALYSIS GUIDELINES:
- If too many results (>1000 hits): Add more specific terms, exclusions, exact phrases
- If too few results (<10 hits): Broaden with synonyms, remove restrictions, use wildcards
- If off-topic results: Add NOT operators, refine domain terms, use exact phrases
- If missing key aspects: Add related concepts with OR operators
- If wrong locations: Adjust geographic scope, add/remove location filters
- If wrong time period: Adjust temporal scope, add recency indicators

Provide:
1. Refined Query: [improved boolean query]
2. Changes Made: [specific modifications and reasoning]
3. Expected Improvement: [how results should be better]
4. Alternative Approaches: [other strategies to try if this doesn't work]

Focus on making targeted improvements that address the specific refinement goal."""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_domain_specific_prompt(
    user_input: str, domain: str, specific_context: str = ""
) -> List[base.Message]:
    """Create domain-specific enhancement prompt.

    Args:
        user_input: User's search input
        domain: Specific domain (business, tech, healthcare, etc.)
        specific_context: Additional context for the domain

    Returns:
        List of Message objects for MCP prompt
    """

    domain_expertise = {
        "business": {
            "key_areas": "Corporate news, earnings, M&A, leadership changes, market performance, regulatory impacts, industry trends, competitive dynamics, supply chain, labor relations, financial performance, strategic initiatives",
            "common_terms": "revenue, profit, earnings, merger, acquisition, IPO, bankruptcy, layoffs, expansion, partnership, investment, valuation, market share",
            "exclusions": "sports business, entertainment business, celebrity business ventures",
        },
        "technology": {
            "key_areas": "Product launches, funding rounds, partnerships, regulatory issues, cybersecurity, AI/ML developments, startup ecosystem, platform changes, infrastructure, research breakthroughs, talent movements",
            "common_terms": "funding, startup, AI, platform, cloud, cybersecurity, innovation, digital transformation, tech stack, scalability, disruption",
            "exclusions": "sports tech, entertainment tech, gaming (unless specifically relevant)",
        },
        "healthcare": {
            "key_areas": "Public health, medical research, healthcare policy, hospital systems, pharmaceutical developments, health technology, regulatory approvals, clinical trials, health emergencies",
            "common_terms": "hospital, clinic, pharmaceutical, FDA approval, clinical trial, public health, medical device, healthcare policy, patient care, medical research",
            "exclusions": "wellness trends, alternative medicine (unless newsworthy), fitness",
        },
        "real_estate": {
            "key_areas": "Market trends, development projects, zoning changes, property sales, regulatory updates, construction, urban planning, housing policy, commercial real estate, investment activity",
            "common_terms": "property, housing, development, zoning, construction, mortgage, real estate market, commercial property, residential, urban planning",
            "exclusions": "vacation rentals, short-term rentals, real estate reality shows",
        },
    }

    domain_info = domain_expertise.get(
        domain.lower(),
        {
            "key_areas": "General domain analysis focusing on key industry factors, major players, regulatory environment, and market dynamics",
            "common_terms": "industry, market, business, development, growth, investment, regulation, policy",
            "exclusions": "entertainment, sports, celebrity news",
        },
    )

    system_message = f"""You are a domain expert in {domain.title()} with deep knowledge of industry dynamics, key players, and critical developments.

DOMAIN EXPERTISE FOR {domain.upper()}:
Key Areas: {domain_info['key_areas']}
Common Terms: {domain_info['common_terms']}
Typical Exclusions: {domain_info['exclusions']}

Your role is to provide sophisticated domain context that enhances search capabilities for {domain} news discovery with specific terminology, industry knowledge, and relevant filtering."""

    user_message = f"""Enhance this search input with {domain} domain expertise:

USER INPUT: "{user_input}"
SPECIFIC CONTEXT: {specific_context or "General " + domain + " context"}

Provide domain-enhanced query with:
- Industry-specific terminology expansion
- Relevant boolean operators and grouping
- Appropriate exclusions for noise reduction
- Location suggestions if relevant to domain
- Time sensitivity considerations for this domain

Focus on creating a query that would find the most relevant {domain} news while filtering out noise."""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]
