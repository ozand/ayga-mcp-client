# ayga-mcp-client

MCP server for Redis API with **29 parsers** across 6 categories.

<!-- MCP Registry identifier -->
mcp-name: io.github.ozand/ayga-mcp-client

## ✨ What's New in v1.2.0

- **29 parsers total** (was 21): Added Search Engine category
- **Search Engines** (8): Google, Yandex, Bing, DuckDuckGo, Baidu, Yahoo, Rambler, You.com
- **FreeAI** (6): Perplexity, GoogleAI, ChatGPT, Kimi, DeepAI, Copilot
- **YouTube** (6): Video metadata, search, suggestions, channel info, comments
- **Translation** (4): Google, DeepL, Bing, Yandex with language control
- **Social media** (4): Telegram groups, Reddit posts/comments
- **Net** (1): HTTP fetcher

## Quick Start

```bash
pip install ayga-mcp-client
```

### Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json` (Linux/macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "ayga": {
      "command": "python",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### VS Code Copilot

Add to your MCP config file (`%APPDATA%\Code\User\mcp.json` on Windows):

```json
{
  "servers": {
    "ayga": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

## Documentation

- **[EXAMPLES.md](EXAMPLES.md)** - Detailed examples with request/response formats for all tools
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Technical architecture and development guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes

## Available Tools

### FreeAI Parsers (6)
- `search_perplexity` - AI-powered search with sources
- `search_googleai` - Google AI search with structured sources
- `search_chatgpt` - ChatGPT with web search
- `search_kimi` - Kimi AI for translation and education
- `search_deepai` - DeepAI multi-style chat
- `search_copilot` - Microsoft Copilot search

### YouTube Parsers (6)
- `parse_youtube_video` - Video metadata, subtitles, comments
- `search_youtube_search` - Search videos by keywords
- `get_youtube_suggest` - Keyword suggestions/autocomplete
- `get_youtube_channel_videos` - List channel videos
- `get_youtube_channel_about` - Channel info from About page
- `parse_youtube_comments` - Parse video comments with threading

### Social Media Parsers (4)
- `scrape_telegram_group` - Scrape public group messages
- `search_reddit_posts` - Search Reddit posts
- `get_reddit_post_info` - Get post with comments
- `search_reddit_comments` - Search Reddit comments

### Translation Services (4)
- `translate_google_translate` - Google Translate (100+ languages)
- `translate_deepl_translate` - DeepL high-quality translation
- `translate_bing_translate` - Microsoft Bing Translator
- `translate_yandex_translate` - Yandex Translate with captcha bypass

### Search Engines (8)
- `search_google_search` - Google search with operators support
- `search_yandex_search` - Yandex search (Russian search engine)
- `search_bing_search` - Bing search with operators support
- `search_duckduckgo_search` - DuckDuckGo privacy-focused search
- `search_baidu_search` - Baidu search (Chinese search engine)
- `search_yahoo_search` - Yahoo search results
- `search_rambler_search` - Rambler search (Russian)
- `search_you_search` - You.com AI-powered search

### Net Parsers (1)
- `fetch_http` - Fetch raw URL content

### Metadata Tools
- `list_parsers` - List all available parsers
- `get_parser_info` - Get parser details
- `health_check` - API health status

## Authentication

Get your API key from https://redis.ayga.tech or contact support@ayga.tech

The client automatically exchanges your API key for a JWT token on first request.

## Example Usage

Once configured, use tools in Claude Desktop or VS Code Copilot:

```
# FreeAI search
@ayga search_perplexity query="latest AI trends 2025" timeout=90
@ayga search_chatgpt query="explain quantum computing" timeout=60

# YouTube parsing
@ayga parse_youtube_video query="https://youtube.com/watch?v=..." preset="default"
@ayga search_youtube_search query="python tutorial" pages_count=2

# Translation with language control
@ayga translate_google_translate query="Hello world" from_language="en" to_language="ru"
@ayga translate_deepl_translate query="Machine learning" to_language="de"

# Social media scraping
@ayga search_reddit_posts query="python" pages_count=1 sort="top"
@ayga scrape_telegram_group query="https://t.me/publicgroup"

# Search engines
@ayga search_google_search query="site:github.com python parser"
@ayga search_yandex_search query="программирование python"
@ayga search_duckduckgo_search query="privacy tools"

# Metadata
@ayga list_parsers
@ayga get_parser_info parser_id="youtube_video"
```

## Environment Variables

- `REDIS_API_KEY` - Your API key (required)
- `REDIS_API_URL` - API URL (default: https://redis.ayga.tech)

## Development

```bash
git clone https://github.com/ozand/ayga-mcp-client.git
cd ayga-mcp-client
pip install -e ".[dev]"

# Run tests
pytest

# Run locally
python -m ayga_mcp_client --username USER --password PASS
```

## License

MIT License - see [LICENSE](LICENSE)

## Links

- [Redis API Documentation](https://redis.ayga.tech/docs)
- [GitHub Repository](https://github.com/ozand/ayga-mcp-client)
- [Report Issues](https://github.com/ozand/ayga-mcp-client/issues)
