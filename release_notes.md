# ayga-mcp-client v1.0.0

First release of **ayga-mcp-client** - MCP server for Redis API with 21+ AI parsers.

## Installation

```bash
pip install ayga-mcp-client
```

## Features

- ✅ 11+ AI parser tools (Perplexity, ChatGPT, Claude, Gemini, Copilot, Grok, DeepSeek, Google Search, Bing, DuckDuckGo, YouTube)
- ✅ Official MCP SDK integration (stdio transport)
- ✅ JWT authentication (username/password or API key)
- ✅ Progressive backoff polling
- ✅ Compatible with Claude Desktop, VS Code Copilot, Cursor
- ✅ Published on PyPI: https://pypi.org/project/ayga-mcp-client/

## Quick Start

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "redis-api": {
      "command": "ayga-mcp-client",
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
      "command": "ayga-mcp-client",
      "args": ["--username", "YOUR_USERNAME", "--password", "YOUR_PASSWORD"]
    }
  }
}
```

## Documentation

- PyPI: https://pypi.org/project/ayga-mcp-client/
- Repository: https://github.com/ozand/ayga-mcp-client
- API Docs: https://redis.ayga.tech/docs

## Changes

- Package renamed from `redis-mcp-client` to `ayga-mcp-client`
- Module renamed from `redis_mcp_client` to `ayga_mcp_client`
- CLI command: `ayga-mcp-client`
- MCP Registry ID: `io.github.ozand/ayga-mcp-client`
