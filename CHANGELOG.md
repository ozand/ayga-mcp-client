# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-12

### Changed
- **Short server name**: Use `@ayga` instead of `@ayga-mcp-client` for easier usage in Claude/VS Code

### Added
- **21 parsers total** (was 11) - full sync with redis_wrapper:
  - **FreeAI (6)**: perplexity, googleai, chatgpt, kimi, deepai, copilot
  - **YouTube (6)**: youtube_video, youtube_search, youtube_suggest, youtube_channel_videos, youtube_channel_about, youtube_comments
  - **Social (4)**: telegram_group, reddit_posts, reddit_post_info, reddit_comments
  - **Translation (4)**: google_translate, deepl_translate, bing_translate, yandex_translate
  - **Net (1)**: http (URL fetcher)

- **Correct tool naming conventions**:
  - FreeAI/Search: `search_{id}` (e.g., `search_perplexity`)
  - YouTube video/comments: `parse_{id}` (e.g., `parse_youtube_video`)
  - YouTube data: `get_{id}` (e.g., `get_youtube_suggest`)
  - Translation: `translate_{id}` (e.g., `translate_google_translate`)
  - Social scraping: `scrape_{id}` (e.g., `scrape_telegram_group`)
  - HTTP: `fetch_{id}` (e.g., `fetch_http`)

- **Extended parameters support**:
  - **YouTube parsers**: `preset`, `interface_language`, `subtitles_language`, `comments_pages`, `pages_count`, `sort`
  - **Translation parsers**: `from_language` (default: "auto"), `to_language` (default: "en")
  - **Social parsers**: `pages_count`, `sort`, `max_comments_count`, `max_empty_posts`
  - All parsers: `preset` parameter support

- **Complete A-Parser name mappings**:
  - YouTube: `SE::YouTube::Video`, `SE::YouTube::Suggest`, `JS::Example::Youtube::Channel::Videos`, etc.
  - Social: `Telegram::GroupScraper`, `Reddit::Posts`, `Reddit::PostInfo`, `Reddit::Comments`
  - Translation: `SE::Google::Translate`, `DeepL::Translator`, `SE::Bing::Translator`, `SE::Yandex::Translate`

### Changed
- Replaced hardcoded 11-parser list with complete 21-parser registry
- Tool generation now uses parser-specific prefixes from PARSERS list
- Input schemas dynamically generated based on parser category
- `submit_parser_task()` now passes extended options to A-Parser task format

### Removed
- Removed non-existent parsers: `claude`, `gemini`, `grok`, `deepseek`, `google_search`, `bing_search`, `duckduckgo`

### Breaking Changes
- Tool names changed for consistency:
  - Old: `search_youtube_search` → New: `search_youtube_search` (unchanged)
  - New tools added: `parse_youtube_video`, `translate_google_translate`, etc.
- Some parsers from v1.0.x no longer available (claude, gemini, grok, deepseek, google_search, bing_search, duckduckgo)

## [1.0.2] - 2026-01-10

### Fixed
- Synchronized `__version__` in `__init__.py` with package version (was 1.0.0, now 1.0.2)
- Removed unused `tools/` directory from package structure

### Maintenance
- Package cleanup and documentation consistency improvements

## [1.0.1] - 2026-01-10

### Fixed
- **Critical**: Fixed parser execution 404 errors
  - Changed `submit_parser_task` to use correct Redis structures API endpoint: `/structures/list/aparser_redis_api/lpush`
  - Changed `get_task_result` to use correct Redis KV API endpoint: `/kv/aparser_redis_api:{task_id}`
  - Updated task submission to match A-Parser task format: `[taskId, parser, preset, query, {}, {}]`
  - Added parser ID mapping (e.g., `perplexity` → `FreeAI::Perplexity`)
  - Improved result parsing to handle A-Parser response format

### Technical Details
- Previously used non-existent `/parsers/{id}/execute` endpoint
- Now uses actual redis_wrapper implementation (Redis queue + KV storage)
- All parser tools (`search_perplexity`, `search_chatgpt`, etc.) now work correctly

## [1.0.0] - 2026-01-10

### Added
- Initial release of **ayga-mcp-client** (renamed from redis-mcp-client)
- MCP server with stdio transport
- 11+ AI parser tools (Perplexity, ChatGPT, Claude, Gemini, etc.)
- HTTP client for Redis API
- Authentication via username/password or API key
- Progressive backoff for task polling
- Metadata tools (list_parsers, get_parser_info, health_check)
- CLI entrypoint: `ayga-mcp-client`
- Support for Claude Desktop, VS Code Copilot, Cursor
- **Published to PyPI**: https://pypi.org/project/ayga-mcp-client/

### Changed
- Package renamed: `redis-mcp-client` → `ayga-mcp-client`
- Module renamed: `redis_mcp_client` → `ayga_mcp_client`
- CLI command: `redis-mcp-client` → `ayga-mcp-client`
- MCP Registry ID: `io.github.ozand/ayga-mcp-client`

### Documentation
- README with quick start guide
- Installation: `pip install ayga-mcp-client`
- Examples for Claude Desktop and VS Code
