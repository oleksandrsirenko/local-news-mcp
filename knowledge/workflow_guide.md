# Local News MCP Workflow Guide

## Recommended Usage Patterns

### Simple Searches (Direct)

- **Use**: `search_news` tool directly
- **When**: You have a well-formed query already
- **Example**:

```json
{
  "q": "technology AND (Apple OR Google)",
  "locations": ["San Francisco, California"],
  "theme": "Tech",
  "from_": "7 days ago"
}
```

### Enhanced Searches (Recommended)

1. **Use**: `enhance-query` prompt with simple input
2. **Get**: Sophisticated query + location/theme suggestions  
3. **Use**: `intelligent_search` tool with enhanced parameters
4. **Result**: More relevant, comprehensive results

### Complex Research Workflows

1. **Use**: `analyze-search-intent` prompt for deep understanding
2. **Use**: `enhance-query` prompt with domain context
3. **Execute**: Multiple searches with variations
4. **Monitor**: `get_latest_headlines` for ongoing developments

## Query Enhancement Examples

### Business Intelligence

- **Input**: "tech layoffs"
- **Enhanced Query**: `technology AND (layoffs OR \"job cuts\" OR downsizing) NOT (hiring OR sports)`
- **JSON Payload**:

```json
{
  "q": "technology AND (layoffs OR \"job cuts\" OR downsizing) NOT (hiring OR sports)",
  "locations": ["San Francisco, California", "Seattle, Washington"],
  "theme": "Tech",
  "detection_methods": ["dedicated_source", "standard_format"],
  "from_": "7 days ago"
}
```

### Real Estate Research

- **Input**: "housing market"
- **Enhanced Query**: `\"real estate\" AND (market OR prices OR sales) NOT (vacation OR rental)`
- **JSON Payload**:

```json
{
  "q": "\"real estate\" AND (market OR prices OR sales) NOT (vacation OR rental)",
  "locations": ["Los Angeles, California", "San Diego, California"],
  "theme": "Business",
  "detection_methods": ["local_section", "standard_format"],
  "from_": "30 days ago"
}
```

### Crisis Monitoring

- **Input**: "port issues"
- **Enhanced Query**: `port AND (delays OR disruption OR closure) AND (shipping OR logistics) NOT airport`
- **JSON Payload**:

```json
{
  "q": "port AND (delays OR disruption OR closure) AND (shipping OR logistics) NOT airport",
  "locations": ["Los Angeles, California", "Long Beach, California"],
  "theme": "Business",
  "detection_methods": ["dedicated_source", "proximity_mention"],
  "from_": "24 hours ago"
}
```

## Pro Tips

- Always specify locations in "City, State" format
- Use theme filters for broad categorization  
- Check `detection_methods` in results for location confidence
- Iterate queries based on result relevance
- Use `workflow-guidance` prompt for complex scenarios

## Available Detection Methods

- `dedicated_source`: Highest confidence, source exclusively covers location
- `local_section`: Location-specific sections in larger publications
- `standard_format`: Standard "City, State" format mentions
- `proximity_mention`: City and state mentioned within 15 words
- `ai_extracted`: AI-detected location mentions (requires AI plan)
- `regional_source`: Regional context for disambiguation

## Theme Categories

Business, Economics, Entertainment, Finance, Health, Politics, Science, Sports, Tech, Crime, Lifestyle, Travel, General.