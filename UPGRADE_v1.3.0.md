# Upgrade to v1.3.0

## Quick Install

```bash
pip install --upgrade ayga-mcp-client
```

Verify installation:
```bash
python -c "import ayga_mcp_client; print(ayga_mcp_client.__version__)"
# Should print: 1.3.0
```

## What's New

### 10 New Parsers Added

**Content Extraction (2 parsers):**
- `parse_article_extractor` - Extract articles with Mozilla Readability algorithm
- `parse_text_extractor` - Parse text blocks with HTML cleaning (2000 queries/min)

**Social Media (6 parsers):**
- `parse_instagram_profile` - Profile data, posts, followers
- `parse_instagram_post` - Post with likes, comments, caption
- `parse_instagram_tag` - Posts by hashtag
- `parse_instagram_geo` - Posts by location
- `search_instagram_search` - Search profiles, hashtags, locations
- `parse_tiktok_profile` - TikTok profile data, videos, followers

**Analytics (1 parser):**
- `get_google_trends` - Keyword trends, regional interest, related queries

**Visual Content (1 parser):**
- `search_pinterest_search` - Pinterest images search (4000+ queries/min)

### Statistics

- **Total parsers:** 29 → 39 (+34% increase)
- **Categories:** 6 → 9 (added Content, Analytics, Visual)
- **All tests passing:** 6/6 ✅

## Configuration

Your existing MCP configuration should work without changes. If not configured yet:

### VS Code (`%APPDATA%\Code\User\mcp.json`)

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

### Claude Desktop

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS/Linux:** `~/.config/Claude/claude_desktop_config.json`

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

## Usage Examples

### Instagram Parsing

```
# Profile with posts and followers
@ayga parse_instagram_profile query="username" timeout=120

# Posts by hashtag
@ayga parse_instagram_tag query="travel" timeout=120

# Posts by location
@ayga parse_instagram_geo query="https://www.instagram.com/explore/locations/..."

# Search
@ayga search_instagram_search query="fashion"
```

**Note:** Some Instagram parsers require authentication cookies. See [EXAMPLES.md](EXAMPLES.md) for details.

### TikTok Parsing

```
# Profile data with videos
@ayga parse_tiktok_profile query="@username" timeout=120
```

### Content Extraction

```
# Extract article with Readability algorithm
@ayga parse_article_extractor query="https://example.com/article"

# Extract text blocks with HTML cleaning
@ayga parse_text_extractor query="https://example.com/page"
```

### Analytics

```
# Single keyword trends
@ayga get_google_trends query="artificial intelligence" timeout=90

# Compare multiple keywords
@ayga get_google_trends query="AI,machine learning,deep learning"
```

### Visual Search

```
# Pinterest image search
@ayga search_pinterest_search query="modern interior design" timeout=60
```

## Breaking Changes

None. All v1.2.0 parsers remain fully compatible.

## Migration Guide

1. **Install v1.3.0:** `pip install --upgrade ayga-mcp-client`
2. **Restart VS Code/Claude Desktop** to reload MCP server
3. **Test new parsers:** Try `@ayga list_parsers` to see all 39 available tools

## Troubleshooting

### Package not updating

```bash
pip uninstall ayga-mcp-client
pip install ayga-mcp-client
```

### MCP server not restarting

- **VS Code:** Restart VS Code completely
- **Claude Desktop:** Quit and relaunch app

### Authentication errors

Verify your API key:
```bash
python -c "import os; print(os.environ.get('REDIS_API_KEY', 'Not set'))"
```

## Documentation

- **Complete Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Development Guide:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **GitHub:** https://github.com/ozand/ayga-mcp-client
- **PyPI:** https://pypi.org/project/ayga-mcp-client/

## Need Help?

- **Issues:** https://github.com/ozand/ayga-mcp-client/issues
- **Email:** support@ayga.tech
