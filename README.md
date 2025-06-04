# Local News MCP Server

A Model Context Protocol (MCP) server for accessing local news data through the NewsCatcher Local News API. This proof-of-concept enables Claude Desktop to search for and retrieve location-specific news articles.

## Features

- **News Search**: Search for articles using advanced queries with boolean operators and location filtering.
- **Latest Headlines**: Get the most recent news headlines for specific locations.
- **Location-Aware**: Filter news by cities, states, or regions.
- **Theme Filtering**: Filter articles by categories (Business, Tech, Politics, Sports, etc.).
- **Rich Formatting**: Articles include summaries, locations, and source information.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- NewsCatcher API key ([get one here](https://www.newscatcherapi.com/pricing))
- Claude Desktop

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/oleksandrsirenko/local-news-mcp.git
cd local-news-mcp

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your NewsCatcher API key
# LOCAL_NEWS_API_KEY=your_actual_api_key_here
```

### 3. Test the Server

```bash
# Run the server locally to test
uv run main.py
```

### 4. Configure Claude Desktop

Create or modify the Claude Desktop configuration file:

**macOS:**

```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**

```powershell
code $env:AppData\Claude\claude_desktop_config.json
```

Add this configuration:

```json
{
  "mcpServers": {
    "local-news": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/local_news_mcp",
        "run",
        "main.py"
      ],
      "env": {
        "LOCAL_NEWS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

>**Important**: Replace `"/absolute/path/to/local_news_mcp"` with the full path to your project directory. You can find this by running `pwd` in your terminal when in the project directory.

### 5. Use with Claude Desktop

Restart Claude Desktop completely. Click Seach and tools button and ensure local-news-mcp tool is enabled.

Try these example queries:

- "What's the latest news in San Francisco?"
- "Show me business news from New York City in the last 7 days"
- "Search for articles about port disruptions in California"

## Available Tools

### `search_news`

Search for news articles with advanced query capabilities.

**Parameters**:

- `q`: Search query with boolean operators (AND, OR, NOT) and wildcards
- `locations`: List of locations (e.g., ["San Francisco, California"])  
- `from_`: Start date (e.g., "7d", "7 days ago", "2025-01-01")
- `theme`: News category filter
- `page_size`: Number of results (1-1000, default: 10)

### `get_latest_headlines`

Get recent headlines for specific locations.

**Parameters**:

- `locations`: List of locations
- `when`: Time period (e.g., "7d", "24h")
- `theme`: News category filter  
- `page_size`: Number of results (1-1000, default: 10)

## Query Examples

### Advanced Search Syntax

- Exact phrases: `\"artificial intelligence\"`
- Boolean operators: `Tesla AND "Elon Musk"`
- Wildcards: `elect*` (finds election, electoral, etc.)
- Complex queries: `(Apple OR Google) AND smartphone NOT lawsuit`

### Location Formats

**Pattern:** "City, Administrative Unit" or "Administrative Unit"

**Examples:**

- US: "San Francisco, California" or "California"
- Canada: "Toronto, Ontario" or "Ontario"
- UK: "Manchester, Greater Manchester" or "Greater Manchester"

## Troubleshooting

### Handle "spawn uv ENOENT" error

If you encounter the "spawn uv ENOENT" error, find the full path to your uv executable with `which uv` and use that path instead:

```json
{
  "mcpServers": {
    "local-news": {
      "command": "/full/path/to/uv",
      "args": [
        "--directory",
        "/absolute/path/to/local_news_mcp",
        "run",
        "main.py"
      ],
      "env": {
        "LOCAL_NEWS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### MCP server is not available

If the local-news server isn't connecting:

1. Check Claude Desktop logs: `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log`
2. Verify your API key is correct
3. Make sure the path to your script is absolute
4. Restart Claude Desktop completely

## Development

This is a proof-of-concept implementation. For production use, consider:

- Better error handling and logging
- Rate limiting and caching
- Configuration management
- Enhanced article formatting
- Additional MCP tools, prompts and resources

## License

MIT License - see LICENSE file for details.

## Contributing

This is a proof-of-concept project. For the production-ready version, please check back later or contact the maintainer.

## Documentation

- [Local News API](https://www.newscatcherapi.com/docs/v3/local-news/overview/introduction)
- [Advanced querying techniques](https://www.newscatcherapi.com/docs/v3/documentation/guides-and-concepts/advanced-querying)