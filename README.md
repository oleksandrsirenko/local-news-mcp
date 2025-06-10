# Local News MCP Server

**Get location-specific news through natural conversation with Claude Desktop.**

Transform simple questions into sophisticated news searches with automatic query enhancement and intelligent clustering.

## ✨ What You Can Ask

Once connected, you can have natural conversations about local news:

- *"What's the latest news about tech layoffs in San Francisco?"*
- *"Show me recent housing market updates in Los Angeles"*
- *"Find news about port disruptions affecting shipping"*
- *"What's happening with real estate in Miami?"*
- *"Any recent business news from Seattle?"*

The server automatically enhances your questions, reduces duplicate stories, and finds the most relevant locations.

## 🚀 Quick Setup

### Prerequisites

- Claude Desktop
- NewsCatcher API key ([get free key](https://www.newscatcherapi.com/pricing))
- Python 3.13+ and [uv](https://docs.astral.sh/uv/)

### Installation

```bash
# 1. Clone and setup
git clone https://github.com/oleksandrsirenko/local-news-mcp.git
cd local-news-mcp
uv venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync

# 2. Add your API key
cp .env.example .env
# Edit .env: LOCAL_NEWS_API_KEY=your_actual_api_key_here

# 3. Test it works
uv run main.py
```

### Claude Desktop Configuration

**macOS:** `~/Library/Application\ Support/Claude/claude_desktop_config.json`  
**Windows:** `%AppData%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "local-news": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/local-news-mcp",
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

**Important:** Replace `/absolute/path/to/local-news-mcp` with your actual project path.

### Restart Claude Desktop

Completely quit and restart Claude Desktop. Look for the 🔌 icon to confirm connection.

## 🔧 How It Works

1. **You ask a simple question** in natural language
2. **Claude automatically enhances your query** using domain expertise
3. **Intelligent clustering** shows diverse stories instead of duplicates
4. **Location detection** finds the most relevant geographic areas
5. **Rich results** include summaries, sentiment, themes, and source confidence

## 🧩 MCP Server Components

This server provides three types of MCP primitives, each with different usage patterns in Claude Desktop:

### 🔧 **Tools** (Model-Controlled)

Claude can automatically use these tools to fetch and analyze news data during conversations.

**Available Tools:**

- `intelligent_search` - Advanced search with clustering and comprehensive coverage
- `search_news` - Direct search with user-provided queries  
- `get_latest_headlines` - Recent headlines for specific locations

*Usage: Claude decides when to use these tools based on your questions. No manual selection is needed.*

### 📖 **Prompts** (User-Controlled)

These help you start conversations and provide structured guidance to Claude.

**Available Prompts:**

- `enhance-query` - Transform simple input into sophisticated search queries.
- `analyze-search-intent` - Understand what you're looking for.
- `workflow-guidance` - Get recommendations for different research approaches.
- `domain-expertise` - Get specialized help for business, tech, politics, etc.
- `competitive-analysis` - Design monitoring strategies for companies.

*Usage: Click the + button in Claude and select these prompts to start enhanced workflows.*

### 📋 **Resources** (Application-Controlled)

Reference materials that Claude can use for context when helping you.

**Available Resources:**

- `knowledge://query-syntax` - Advanced query construction guide
- `guide://workflow` - Complete usage guide and best practices

*Usage: Claude Desktop requires you to explicitly add these before Claude can reference them. Click + and select them when you need query syntax help or usage guidance.*

### **How to Use in Claude Desktop**

1. **For Quick Questions**: Just ask naturally - Claude will use tools automatically
   - *"What's happening with tech layoffs in San Francisco?"*

2. **For Enhanced Research**: Start with a prompt
   - Click **+** → Select `enhance-query` → Enter simple topic
   - Use the enhanced query with Claude's automatic tool usage

3. **For Complex Analysis**: Combine prompts and resources
   - Add `guide://workflow` resource for methodology guidance
   - Use `domain-expertise` prompt for specialized research
   - Ask follow-up questions - Claude will use tools automatically

## Testing

### Run all tests

```bash
./test_runner.sh
```

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv --directory . run main.py
```

## 🛠 Troubleshooting

### "spawn uv ENOENT" Error

Find your uv path and use it in config:

```bash
which uv  # Use this full path in Claude config
```

### Server Not Connecting

1. Verify API key in `.env` file
2. Check absolute path in Claude configuration  
3. Restart Claude Desktop completely
4. Check logs: `tail -f ~/Library/Logs/Claude/mcp*.log`

### No Results or Poor Quality

The server automatically optimizes queries, but you can be more specific:

- *"Business news in downtown Seattle"* (more specific location)
- *"Tech startup funding in Silicon Valley"* (specific domain + location)
- *"Real estate prices in Miami last week"* (timeframe)

## 🏗 Development

```bash
# Run development server
uv run mcp dev main.py

# Install in Claude Desktop for testing
uv run mcp install main.py --name "local-news-dev"
```

## 🌐 API Reference

Built on [NewsCatcher Local News API](https://www.newscatcherapi.com/docs/v3/local-news) with intelligent query enhancement and clustering.

**Location Detection Methods:**

- `dedicated_source`: Exclusive local coverage (highest confidence)
- `local_section`: Location-specific news sections 
- `standard_format`: "City, State" mentions
- `proximity_mention`: Geographic terms within 15 words
- `ai_extracted`: AI-detected locations (premium feature)
- `regional_source`: Regional publication context

**Available Themes:**

Business, Economics, Entertainment, Finance, Health, Politics, Science, Sports, Tech, Crime, Lifestyle, Travel, General

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This server demonstrates advanced MCP capabilities including intelligent query processing, clustering, and domain expertise. Contributions welcome for additional domains and enhancement strategies.