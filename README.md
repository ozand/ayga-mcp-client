# redis-mcp-client

MCP server for Redis API with 21+ AI parsers.

<!-- MCP Registry identifier -->
mcp-name: io.github.ozand/redis-mcp-client

## Installation

\\\ash
pip install redis-mcp-client
\\\

## Quick Start

### Claude Desktop

Add to \~/.config/Claude/claude_desktop_config.json\ (Linux/macOS) or \%APPDATA%\Claude\claude_desktop_config.json\ (Windows):

\\\json
{
  "mcpServers": {
    "redis-api": {
      "command": "redis-mcp-client",
      "args": ["--username", "YOUR_USERNAME", "--password", "YOUR_PASSWORD"]
    }
  }
}
\\\

### VS Code Copilot

Add to \.vscode/mcp.json\:

\\\json
{
  "servers": {
    "redis-api": {
      "command": "redis-mcp-client",
      "args": ["--username", "YOUR_USERNAME", "--password", "YOUR_PASSWORD"]
    }
  }
}
\\\

### Cursor IDE

Same config as Claude Desktop in Cursor settings.

## Available Tools

### AI Parsers (21)
- \search_perplexity\ - Perplexity AI search with sources
- \search_chatgpt\ - ChatGPT with web search
- \search_claude\ - Claude AI analysis
- \search_gemini\ - Google Gemini
- \search_copilot\ - Microsoft Copilot
- \search_grok\ - xAI Grok
- \search_deepseek\ - DeepSeek AI
- \google_search\ - Google Search results
- \ing_search\ - Bing Search results
- \youtube_search\ - YouTube video search
- \youtube_video_info\ - Video metadata and transcripts
- \eddit_posts\ - Reddit post search
- \eddit_comments\ - Reddit comment search
- \	elegram_messages\ - Telegram channel scraping
- And more...

### Redis Operations
- \edis_get\ / \edis_set\ - Key-value operations
- \edis_list_push\ / \edis_list_pop\ - List operations
- \edis_hash_set\ / \edis_hash_get\ - Hash operations

### Metadata
- \list_parsers\ - List all available parsers
- \get_parser_info\ - Get parser details and parameters
- \health_check\ - API health status

## Authentication

Get credentials from: support@ayga.tech

## Configuration

Environment variables:
- \REDIS_API_URL\ - API URL (default: https://redis.ayga.tech)
- \REDIS_USERNAME\ - Username
- \REDIS_PASSWORD\ - Password
- \REDIS_API_KEY\ - API key (alternative to username/password)

## License

MIT
