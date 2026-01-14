# ayga-mcp-client

MCP server for Redis API with **40 parsers** across 9 categories.

<!-- MCP Registry identifier -->
mcp-name: io.github.ozand/ayga-mcp-client

## ✨ What's New in v1.4.0

- **40 parsers total** (was 39): Added Link Extractor for domain scraping workflows
- **+1 parser**: Link Extractor with multi-level crawling and filtering
- **Content** (3): Article extractor, Text extractor, Link extractor (NEW)
- **Link Extractor features**:
  - Multi-level crawling (depth 1-5)
  - Internal/external link filtering
  - Automatic deduplication
  - 3 presets: default, deep_crawl, all_links
- **Agent Orchestration**: Optimized for AI agents to orchestrate domain content scraping
- **Social media** (10): Instagram (6), TikTok (1), Telegram, Reddit (3)
- **Analytics** (1): Google Trends for keyword research
- **Visual** (1): Pinterest search for images
- **Search Engines** (8): Google, Yandex, Bing, DuckDuckGo, Baidu, Yahoo, Rambler, You.com
- **FreeAI** (6): Perplexity, GoogleAI, ChatGPT, Kimi, DeepAI, Copilot
- **YouTube** (6): Video metadata, search, suggestions, channel info, comments
- **Translation** (4): Google, DeepL, Bing, Yandex with language control
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

### Social Media Parsers (10)
- `scrape_telegram_group` - Scrape public group messages
- `search_reddit_posts` - Search Reddit posts with sorting
- `get_reddit_post_info` - Get post with comments and details
- `search_reddit_comments` - Search Reddit comments
- `parse_instagram_profile` - Profile data, posts, followers (requires auth cookie)
- `parse_instagram_post` - Post with likes, comments, caption
- `parse_instagram_tag` - Posts by hashtag (requires auth cookie)
- `parse_instagram_geo` - Posts by location with coordinates
- `search_instagram_search` - Search profiles, hashtags, locations
- `parse_tiktok_profile` - TikTok profile data, videos, followers

### Translation Services (4)
- `translate_google_translate` - Google Translate (100+ languages)
- `translate_deepl_translate` - DeepL high-quality translation
- `translate_bing_translate` - Microsoft Bing Translator
- `translate_yandex_translate` - Yandex Translate with captcha bypass

### Search Engines (8)
- `search_google_search` - Google search with operators support
- `search_yandex_search` - Yandex search (Russian search engine)
- `search_bing_search` - Bing search with operators support
- `search_duckduckgo_search` - Privacy-focused DuckDuckGo search
- `search_baidu_search` - Chinese search engine Baidu
- `search_yahoo_search` - Yahoo search results
- `search_rambler_search` - Russian search engine Rambler
- `search_you_search` - You.com AI-powered search

### Content Parsers (3)
- `parse_article_extractor` - Extract articles with Mozilla Readability algorithm
- `parse_text_extractor` - Parse text blocks with automatic HTML cleaning (2000 queries/min)
- `extract_link_extractor` - Extract all links from HTML pages with filtering and deduplication ✨ *NEW*

### Analytics Parsers (1)
- `get_google_trends` - Parse trending keywords, interest data, regional trends

### Visual Content Parsers (1)
- `search_pinterest_search` - Pinterest images, titles, descriptions (4000+ queries/min)

### Net Tools (1)
- `fetch_http` - Fetch raw URL content
### Net Tools (1)
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

# Instagram/TikTok (Social Media)
@ayga parse_instagram_profile query="username" timeout=120
@ayga parse_instagram_tag query="travel" timeout=120
@ayga parse_tiktok_profile query="@username"

# Translation with language control
@ayga translate_google_translate query="Hello world" from_language="en" to_language="ru"
@ayga translate_deepl_translate query="Machine learning" to_language="de"

# Content extraction
@ayga parse_article_extractor query="https://example.com/article"
@ayga parse_text_extractor query="https://example.com/page"

# Analytics and trends
@ayga get_google_trends query="artificial intelligence" timeout=90
@ayga get_google_trends query="AI,machine learning,deep learning"

# Visual content
@ayga search_pinterest_search query="modern interior design" timeout=60

# Social media
@ayga parse_instagram_profile query="username" timeout=120
@ayga search_reddit_posts query="python" pages_count=1 sort="top"

# Search engines
@ayga search_google_search query="site:github.com python parser"
@ayga search_yandex_search query="программирование python"

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
