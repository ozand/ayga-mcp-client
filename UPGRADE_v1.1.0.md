# Updating Your MCP Configuration for v1.1.0

If you're using ayga-mcp-client v1.0.x and want to upgrade to v1.1.0, follow these steps.

## 1. Install/Upgrade Package

```bash
pip install --upgrade ayga-mcp-client
```

Or for development:
```bash
cd t:\Code\python\A-PARSER\ayga-mcp-client
pip install -e .
```

## 2. Verify Installation

```bash
python -m ayga_mcp_client --help
```

Or check version:
```python
import ayga_mcp_client
print(ayga_mcp_client.__version__)  # Should be 1.1.0
```

## 3. Update MCP Configuration (if needed)

Your existing configuration should continue to work without changes:

### VS Code (`%APPDATA%\Code\User\mcp.json`)

```json
{
  "servers": {
    "ayga": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "GnYEheuF3hs_k_GbQgtTy_LFAB2b3GaSx1PA49u_JOg"
      }
    }
  }
}
```

### Claude Desktop

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ayga": {
      "command": "python",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "GnYEheuF3hs_k_GbQgtTy_LFAB2b3GaSx1PA49u_JOg"
      }
    }
  }
}
```

## 4. Restart Your Editor/Client

- **VS Code**: Reload window (Ctrl+Shift+P → "Reload Window")
- **Claude Desktop**: Restart application
- **Cursor**: Restart application

## 5. Test New Parsers

Try one of the new tools to verify everything works:

```
# In chat with MCP enabled:
@ayga list_parsers

# Test YouTube parser
@ayga get_youtube_suggest query="programming" timeout=30

# Test Translation
@ayga translate_google_translate query="Hello world" from_language="en" to_language="ru"

# Test Social Media
@ayga search_reddit_posts query="python" pages_count=1
```

## 6. Explore New Features

### YouTube Parsers (6 total)

```
# Get video metadata
@ayga parse_youtube_video query="https://youtube.com/watch?v=dQw4w9WgXcQ" preset="default"

# Search videos
@ayga search_youtube_search query="python tutorial" pages_count=2 sort="relevance"

# Get keyword suggestions (ultra-fast)
@ayga get_youtube_suggest query="machine learning" timeout=10

# Get channel videos
@ayga get_youtube_channel_videos query="https://youtube.com/@Fireship"

# Get channel info
@ayga get_youtube_channel_about query="https://youtube.com/@Fireship/about"

# Parse comments
@ayga parse_youtube_comments query="https://youtube.com/watch?v=..." pages=2
```

### Translation (4 services)

```
# Google Translate (100+ languages, fastest)
@ayga translate_google_translate query="Hello world" from_language="en" to_language="ru"

# DeepL (highest quality, 30+ languages)
@ayga translate_deepl_translate query="Machine learning" from_language="en" to_language="de"

# Bing Translator
@ayga translate_bing_translate query="Artificial intelligence" to_language="es"

# Yandex Translate (90+ languages, captcha bypass)
@ayga translate_yandex_translate query="Deep learning" to_language="zh"
```

### Social Media (4 parsers)

```
# Scrape Telegram group
@ayga scrape_telegram_group query="https://t.me/publicgroup"

# Search Reddit posts
@ayga search_reddit_posts query="python" pages_count=2 sort="top"

# Get specific Reddit post with comments
@ayga get_reddit_post_info query="https://reddit.com/r/python/comments/..." max_comments_count=100

# Search Reddit comments
@ayga search_reddit_comments query="asyncio" pages_count=1
```

## Troubleshooting

### Issue: Tools not appearing

**Solution**: Restart your editor/client after upgrading the package.

### Issue: Old tool names not working

**Solution**: v1.1.0 removed non-existent parsers (claude, gemini, grok, etc.). Use alternatives:
- `claude` → `search_chatgpt` or `search_perplexity`
- `gemini` → `search_googleai`
- `google_search` → `search_googleai` or `search_perplexity`

### Issue: "Tool is disabled" error

**Solution**: Some tools may need to be enabled in your MCP configuration. Check the client logs.

### Issue: Timeouts on YouTube parsers

**Solution**: YouTube parsers can be slow (30-90s). Use higher timeout values:
```
@ayga search_youtube_search query="..." timeout=120
```

## What's Next?

- Explore all 21 parsers with `@ayga list_parsers`
- Get detailed parser info: `@ayga get_parser_info parser_id="youtube_video"`
- Check API health: `@ayga health_check`

## Need Help?

- **Documentation**: https://redis.ayga.tech/docs
- **Issues**: https://github.com/ozand/ayga-mcp-client/issues
- **Support**: support@ayga.tech
