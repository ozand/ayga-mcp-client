# Release Notes: ayga-mcp-client v1.1.0

**Release Date:** January 12, 2026

## 🎉 Major Update: 21 Parsers with Extended Parameters

This release brings ayga-mcp-client to full feature parity with redis_wrapper, adding **10 new parsers** across YouTube, Translation, and Social Media categories, plus extended parameter support for advanced use cases.

---

## ✨ New Features

### 10 New Parsers Added

**YouTube (5 new parsers):**
- `parse_youtube_video` - Extract video metadata, subtitles, comments
- `get_youtube_suggest` - Get keyword suggestions (ultra-fast: 1-3s)
- `get_youtube_channel_videos` - List all channel videos
- `get_youtube_channel_about` - Get channel info, stats, social links
- `parse_youtube_comments` - Parse video comments with threading support

**Translation (4 new parsers):**
- `translate_google_translate` - Google Translate (100+ languages, 2600 q/min)
- `translate_deepl_translate` - DeepL high-quality translation (30+ languages)
- `translate_bing_translate` - Microsoft Bing Translator (100+ languages)
- `translate_yandex_translate` - Yandex Translate with captcha bypass (90+ languages)

**Social Media (4 new parsers):**
- `scrape_telegram_group` - Scrape public Telegram groups
- `search_reddit_posts` - Search Reddit posts by keyword/subreddit
- `get_reddit_post_info` - Get specific post with nested comments
- `search_reddit_comments` - Search Reddit comments

**Net (1 new parser):**
- `fetch_http` - Fetch raw URL content

### Extended Parameters Support

All parsers now support category-specific parameters:

**YouTube Parsers:**
```json
{
  "query": "https://youtube.com/watch?v=...",
  "preset": "default",
  "interface_language": "en",
  "subtitles_language": "en",
  "comments_pages": 5,
  "pages_count": 2,
  "sort": "relevance"
}
```

**Translation Parsers:**
```json
{
  "query": "Hello world",
  "from_language": "en",
  "to_language": "ru",
  "preset": "default"
}
```

**Social Media Parsers:**
```json
{
  "query": "python",
  "pages_count": 3,
  "sort": "top",
  "max_comments_count": 500
}
```

### Correct Tool Naming Convention

Tools now use category-specific prefixes:
- **Search**: `search_{id}` (FreeAI, YouTube search, Reddit, etc.)
- **Parse**: `parse_{id}` (YouTube video/comments)
- **Get**: `get_{id}` (YouTube suggest/channel, Reddit post)
- **Translate**: `translate_{id}` (all translation services)
- **Scrape**: `scrape_{id}` (Telegram groups)
- **Fetch**: `fetch_{id}` (HTTP content)

### Complete A-Parser Mappings

All 21 parsers now have correct A-Parser name mappings:
- `youtube_video` → `SE::YouTube::Video`
- `telegram_group` → `Telegram::GroupScraper`
- `google_translate` → `SE::Google::Translate`
- `reddit_posts` → `Reddit::Posts`
- etc.

---

## 🔄 Changes

### Replaced Parsers

**Removed (non-existent in redis_wrapper):**
- `search_claude`
- `search_gemini`
- `search_grok`
- `search_deepseek`
- `search_google_search`
- `search_bing_search`
- `search_duckduckgo`

**Added (actual redis_wrapper parsers):**
- `search_googleai` (Google AI Mode)
- `search_kimi` (Kimi AI)
- `search_deepai` (DeepAI)
- All YouTube, Translation, Social, Net parsers (listed above)

### Tool Generation

- Tool schemas now dynamically generated based on parser category
- Extended parameters automatically included in input schemas
- Tool names constructed from parser-specific prefixes

---

## 🐛 Bug Fixes

- Fixed hardcoded `search_` prefix for all tools (now uses correct category prefix)
- Fixed tool call matching to support all prefix types
- Fixed parameter passing to A-Parser task format (now includes options dict)

---

## 📊 Statistics

- **Total Parsers**: 21 (was 11)
- **Categories**: 5 (FreeAI, YouTube, Social, Translation, Net)
- **Total Tools**: 24 (21 parsers + 3 metadata tools)
- **Extended Parameters**: 10+ new optional parameters across categories
- **Test Coverage**: 6/6 tests passing

---

## 🚀 Upgrading

### From v1.0.x

```bash
pip install --upgrade ayga-mcp-client
```

**Breaking Changes:**
- Some parsers removed (claude, gemini, grok, deepseek, google_search, bing_search, duckduckgo)
- Tool names unchanged for existing parsers
- New tools added with category-specific prefixes

**Migration Guide:**
- If using removed parsers, switch to available alternatives:
  - `claude` → `search_chatgpt` or `search_perplexity`
  - `gemini` → `search_googleai`
  - `grok`/`deepseek` → `search_chatgpt` or `search_kimi`
  - `google_search`/`bing_search` → `search_googleai` or `search_perplexity`

---

## 📖 Documentation

- **README.md** - Updated with all 21 parsers
- **CHANGELOG.md** - Complete v1.1.0 changelog
- **EXAMPLES.md** - Examples for new parsers (to be updated)
- **Test Suite** - `tests/test_v1_1_0_parsers.py` validates all changes

---

## 🔗 Links

- **PyPI**: https://pypi.org/project/ayga-mcp-client/
- **GitHub**: https://github.com/ozand/ayga-mcp-client
- **API Docs**: https://redis.ayga.tech/docs
- **Support**: support@ayga.tech

---

## 🙏 Acknowledgments

This release brings full synchronization with the [redis_wrapper](https://github.com/ozand/redis_wrapper) backend, ensuring all production parsers are available through the MCP interface.

---

**Full Changelog**: [v1.0.2...v1.1.0](https://github.com/ozand/ayga-mcp-client/compare/v1.0.2...v1.1.0)
