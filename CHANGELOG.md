# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### Added
- Initial release
- MCP server with stdio transport
- Support for 21+ AI parsers:
  - Perplexity AI, ChatGPT, Claude, Gemini, Copilot, Grok, DeepSeek
  - Google Search, Bing, DuckDuckGo
  - YouTube Search and Video Info
  - Reddit Posts, Comments, Post Info
  - Telegram Messages
  - Bing/Google/DeepL/Yandex Translation
  - HTTP Fetcher
- Redis operations (get/set)
- Metadata tools (list parsers, get info, health check)
- Authentication via username/password or API key
- Progressive backoff polling for async results
- GitHub Actions for CI/CD
- PyPI publishing workflow

### Security
- JWT token-based authentication
- API key support
- Environment variable configuration
