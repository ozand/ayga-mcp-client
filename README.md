# redis-mcp-client

MCP server for Redis API with 21+ AI parsers.

<!-- MCP Registry identifier -->
mcp-name: io.github.ozand/redis-mcp-client

## Quick Start

```bash
pip install redis-mcp-client
```

### Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json` (Linux/macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "redis-api": {
      "command": "redis-mcp-client",
      "args": ["--username", "YOUR_USERNAME", "--password", "YOUR_PASSWORD"]
    }
  }
}
```

### VS Code Copilot

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "redis-api": {
      "command": "redis-mcp-client",
      "args": ["--username", "YOUR_USERNAME", "--password", "YOUR_PASSWORD"]
    }
  }
}
```

## Available Tools

### AI Parsers (11+)
- `search_perplexity` - Perplexity AI search
- `search_chatgpt` - ChatGPT with web search
- `search_claude` - Claude AI
- `search_gemini` - Google Gemini
- `search_copilot` - Microsoft Copilot
- `search_grok` - xAI Grok
- `search_deepseek` - DeepSeek AI
- `search_google_search` - Google web search
- `search_bing_search` - Bing search
- `search_duckduckgo` - DuckDuckGo
- `search_youtube_search` - YouTube search

### Metadata Tools
- `list_parsers` - List all available parsers
- `get_parser_info` - Get parser details
- `health_check` - API health status

## Authentication

Get credentials: support@ayga.tech or create account at https://redis.ayga.tech

## Environment Variables

- `REDIS_API_URL` - API URL (default: https://redis.ayga.tech)
- `REDIS_USERNAME` - Username
- `REDIS_PASSWORD` - Password
- `REDIS_API_KEY` - API key (alternative to username/password)

## Development

```bash
git clone https://github.com/ozand/redis-mcp-client.git
cd redis-mcp-client
pip install -e ".[dev]"

# Run tests
pytest

# Run locally
python -m redis_mcp_client --username USER --password PASS
```

## License

MIT License - see [LICENSE](LICENSE)

## Links

- [Redis API Documentation](https://redis.ayga.tech/docs)
- [GitHub Repository](https://github.com/ozand/redis-mcp-client)
- [Report Issues](https://github.com/ozand/redis-mcp-client/issues)
