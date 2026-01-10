# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
