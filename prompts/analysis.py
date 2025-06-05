"""Analysis and intent detection prompts for Local News MCP server.

This module provides prompt creators for understanding user intent,
domain analysis, and competitive intelligence workflows.
"""

from typing import List
from mcp.server.fastmcp.prompts import base


def create_intent_analysis_prompt(user_input: str) -> List[base.Message]:
    """Create comprehensive intent analysis prompt.

    Args:
        user_input: User's search input to analyze

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = """You are a search intent analysis expert specializing in news and information discovery. Analyze user input to understand the complete search context and requirements.

ANALYSIS FRAMEWORK:

1. **Domain Classification**
   - Primary industry/sector (Technology, Business, Politics, Health, etc.)
   - Secondary domains if applicable
   - Cross-domain implications

2. **Entity Extraction**
   - Companies, organizations, institutions
   - People, executives, public figures  
   - Geographic locations (cities, states, regions)
   - Events, initiatives, programs
   - Products, services, technologies

3. **Intent Categories**
   - Information seeking (what, who, where, when, how)
   - Monitoring (ongoing developments, trends)
   - Analysis (impact, implications, comparisons)
   - Crisis/Alert (breaking news, emergencies)
   - Research (background, historical context)

4. **Temporal Sensitivity**
   - Breaking/Real-time (within hours)
   - Recent (days to weeks)
   - Trending (weeks to months)
   - Historical (months to years)
   - Predictive (future implications)

5. **Geographic Scope**
   - Hyperlocal (neighborhood, district)
   - Local (city, metropolitan area)
   - Regional (state, multi-state area)
   - National (country-wide)
   - International (global implications)

6. **Information Depth**
   - Headlines only
   - Summary coverage
   - Detailed analysis
   - Comprehensive research
   - Expert commentary

7. **Sentiment Interest**
   - Neutral reporting
   - Positive developments
   - Negative impacts/risks
   - Controversial issues
   - Crisis situations

OUTPUT FORMAT:
Provide structured analysis:
- Primary Domain: [main category]
- Key Entities: [companies, people, places, events]
- Intent Type: [information/monitoring/analysis/crisis/research]
- Time Sensitivity: [breaking/recent/trending/historical]
- Geographic Focus: [hyperlocal/local/regional/national/international]
- Information Depth: [headlines/summary/detailed/comprehensive]
- Sentiment Preference: [neutral/positive/negative/controversial/crisis]
- Search Complexity: [simple/moderate/complex]
- Recommended Approach: [workflow suggestions]"""

    user_message = f"""Analyze this search input comprehensively:

INPUT: "{user_input}"

Provide a complete intent analysis that will inform query enhancement and search strategy. Consider:
- What is the user really trying to understand or discover?
- What context might they be missing?
- What related aspects should be considered?
- How urgent or time-sensitive is this query?
- What level of detail are they likely seeking?"""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_domain_analysis_prompt(
    domain: str, specific_context: str = ""
) -> List[base.Message]:
    """Create domain-specific analysis prompt.

    Args:
        domain: Specific domain (business, tech, healthcare, etc.)
        specific_context: Additional context for the domain

    Returns:
        List of Message objects for MCP prompt
    """

    domain_expertise = {
        "business": """Key areas: Corporate news, earnings, M&A, leadership changes, market performance, regulatory impacts, industry trends, competitive dynamics, supply chain, labor relations, financial performance, strategic initiatives""",
        "technology": """Key areas: Product launches, funding rounds, partnerships, regulatory issues, cybersecurity, AI/ML developments, startup ecosystem, platform changes, infrastructure, research breakthroughs, talent movements, industry disruption""",
        "real_estate": """Key areas: Market trends, development projects, zoning changes, property sales, regulatory updates, construction, urban planning, housing policy, commercial real estate, investment activity, demographic shifts""",
        "politics": """Key areas: Elections, policy changes, legislation, regulatory updates, government appointments, political campaigns, voting, public policy, budget decisions, administrative actions, political controversies""",
        "healthcare": """Key areas: Public health, medical research, healthcare policy, hospital systems, pharmaceutical developments, health technology, regulatory approvals, clinical trials, health emergencies, healthcare access""",
    }

    system_message = f"""You are a domain expert in {domain.title()} with deep knowledge of industry dynamics, key players, and critical developments.

DOMAIN EXPERTISE:
{domain_expertise.get(domain.lower(), "General domain analysis focusing on key industry factors, major players, regulatory environment, and market dynamics.")}

Your role is to provide sophisticated domain context that enhances search capabilities for {domain} news discovery."""

    user_message = f"""Provide domain expertise for {domain} news searches.

SPECIFIC CONTEXT: {specific_context}

Include:
- Key terminology and industry jargon
- Major players and organizations to consider
- Typical news patterns and cycles
- Important regulatory or market factors
- Related domains that often intersect
- Common search refinements for this domain

This analysis will inform query enhancement for more relevant news discovery."""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_competitive_analysis_prompt(
    companies: List[str], analysis_focus: str = "general"
) -> List[base.Message]:
    """Create competitive landscape analysis prompt.

    Args:
        companies: List of companies to analyze
        analysis_focus: Type of analysis (general, market, financial, etc.)

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = """You are a competitive intelligence analyst specializing in news-based market analysis. Provide strategic guidance for tracking competitive developments through local and industry news."""

    user_message = f"""Design a competitive analysis approach for tracking these companies through news:

COMPANIES: {', '.join(companies)}
ANALYSIS FOCUS: {analysis_focus}

Recommend:
- Key search terms and query strategies
- Important news categories to monitor
- Geographic markets to focus on
- Timing and frequency considerations
- Competitive intelligence indicators to track
- Alert triggers for significant developments"""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_market_research_prompt(
    industry: str, research_objectives: List[str], geographic_scope: str = "national"
) -> List[base.Message]:
    """Create market research analysis prompt.

    Args:
        industry: Industry to research
        research_objectives: List of research goals
        geographic_scope: Geographic focus for research

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = """You are a market research analyst specializing in news-based industry intelligence. Design comprehensive research strategies using local news sources for market insights."""

    user_message = f"""Design a market research approach for this industry:

INDUSTRY: {industry}
RESEARCH OBJECTIVES: {', '.join(research_objectives)}
GEOGRAPHIC SCOPE: {geographic_scope}

Provide:
- Industry-specific search strategies
- Key market indicators to track through news
- Regional focus areas for local news monitoring
- Timeline and frequency recommendations
- Data collection and analysis frameworks
- Early warning indicators for market shifts"""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_crisis_monitoring_prompt(
    alert_keywords: List[str],
    geographic_areas: List[str],
    severity_indicators: List[str],
) -> List[base.Message]:
    """Create crisis monitoring and early warning prompt.

    Args:
        alert_keywords: Keywords that indicate potential crisis
        geographic_areas: Areas to monitor
        severity_indicators: Indicators of crisis severity

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = """You are a crisis monitoring specialist. Design early warning systems using local news sources to detect and assess emerging crisis situations."""

    user_message = f"""Design a crisis monitoring system for these parameters:

ALERT KEYWORDS: {', '.join(alert_keywords)}
GEOGRAPHIC AREAS: {', '.join(geographic_areas)}
SEVERITY INDICATORS: {', '.join(severity_indicators)}

Recommend:
- Early detection query strategies
- Escalation triggers and thresholds
- Geographic monitoring priorities
- Source reliability assessment
- Real-time alert mechanisms
- Crisis severity classification system"""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]


def create_trend_analysis_prompt(
    topic: str, time_horizon: str = "6 months", trend_indicators: List[str] = None
) -> List[base.Message]:
    """Create trend analysis and pattern detection prompt.

    Args:
        topic: Topic to analyze for trends
        time_horizon: Time period for trend analysis
        trend_indicators: Specific indicators to track

    Returns:
        List of Message objects for MCP prompt
    """

    system_message = """You are a trend analysis expert specializing in pattern detection through news coverage. Identify emerging trends and forecast developments using local news intelligence."""

    indicators = trend_indicators or [
        "frequency",
        "sentiment",
        "geographic spread",
        "source diversity",
    ]

    user_message = f"""Design a trend analysis approach for this topic:

TOPIC: {topic}
TIME HORIZON: {time_horizon}
TREND INDICATORS: {', '.join(indicators)}

Provide:
- Trend detection methodologies
- Key metrics and indicators to track
- Geographic pattern analysis strategies
- Temporal analysis frameworks
- Signal vs noise filtering techniques
- Predictive indicators for trend evolution"""

    return [base.SystemMessage(system_message), base.UserMessage(user_message)]
