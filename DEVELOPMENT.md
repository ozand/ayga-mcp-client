# Development Context

## Project Origin

**ayga-mcp-client** (formerly redis-mcp-client) - MCP server providing unified access to Redis API with 21+ AI parsers for Claude Desktop, VS Code Copilot, and Cursor.

### Why This Project Exists

**Problem**: Original `redis_wrapper` project had custom MCP implementation (5100+ lines) that was:
- Only accessible via stdio (not discoverable by LLM clients)
- Tightly coupled to FastAPI backend
- Difficult to distribute and install

**Solution**: Separate, lightweight MCP client package:
- Published on PyPI for easy installation: `pip install ayga-mcp-client`
- Uses official `mcp` SDK (not FastMCP - that doesn't exist)
- Clean separation: API backend (redis_wrapper) + MCP client (ayga-mcp-client)
- Compatible with all MCP clients (Claude Desktop, Copilot, Cursor)

## Architecture Decisions

### 1. Why Official MCP SDK?

Initially explored "FastMCP" but discovered it doesn't exist as a standard package. The correct approach is using the official `mcp` SDK from Anthropic.

**Key imports**:
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
```

### 2. Why stdio Transport Only?

MCP protocol supports multiple transports, but **stdio is the only one supported by LLM clients** (Claude Desktop, Copilot, Cursor). HTTP/SSE/WebSocket won't work for these clients.

### 3. Why Separate Repository?

- **Decoupling**: API backend can evolve independently from MCP client
- **Distribution**: PyPI package can be installed without cloning entire backend
- **Versioning**: Independent versioning and releases
- **Clarity**: Each repo has single responsibility

### 4. Package Naming: redis-mcp-client → ayga-mcp-client

Original name referenced implementation detail (Redis). New name reflects the brand (Ayga) and is more memorable.

## Technical Implementation

### Authentication Flow

1. Client connects via stdio
2. First API call: authenticate with username/password OR api_key
3. Receive JWT token (stored in client instance)
4. All subsequent calls use JWT Bearer token

```python
# Username/password
async def _login(self) -> str:
    response = await self.client.post("/auth/login", ...)
    return response.json()["access_token"]

# API key
async def _exchange_api_key(self) -> str:
    response = await self.client.post("/auth/exchange", ...)
    return response.json()["access_token"]
```

### Task Submission & Polling

AI parsers run asynchronously via A-Parser (Windows app polling Redis queue):

1. **Submit**: `POST /parsers/{parser_id}/submit` → returns `query_id`
2. **Poll**: `GET /parsers/{parser_id}/result/{query_id}` with progressive backoff:
   - 1 second intervals for first 10 attempts
   - Then 3 second intervals
   - Timeout after 60 seconds

```python
async def wait_for_result(self, parser_id: str, query_id: str) -> dict:
    max_wait = 60
    check_interval = 1
    # Progressive backoff logic...
```

### Parser Tools

11 AI parser tools + 3 metadata tools:

**Parsers**: perplexity, chatgpt, claude, gemini, copilot, grok, deepseek, google_search, bing_search, duckduckgo, youtube_search

**Metadata**: list_parsers, get_parser_info, health_check

Tools are dynamically generated from `PARSERS` list in `server.py`.

## Project Structure

```
ayga-mcp-client/
├── src/
│   └── ayga_mcp_client/
│       ├── __init__.py          # Exports: create_mcp_server, RedisAPIClient
│       ├── __main__.py          # CLI entrypoint with argparse
│       ├── server.py            # MCP server implementation
│       ├── api/
│       │   └── client.py        # HTTP client for Redis API
│       └── tools/               # Reserved for future extensions
├── tests/
│   └── test_basic.py            # Basic unit tests
├── pyproject.toml               # Package metadata (setuptools)
├── README.md                    # User-facing documentation
└── CHANGELOG.md                 # Version history
```

## Build & Publish

### Requirements

- Python 3.11+
- setuptools<75.0 (for Metadata-Version 2.1 compatibility with twine)
- Dependencies: `mcp>=1.0.0`, `httpx>=0.27.0`, `pydantic>=2.0.0`

### Build Process

```bash
# Clean build artifacts
rm -rf dist/ build/ src/ayga_mcp_client.egg-info/

# Build
python -m build

# Check
twine check dist/*

# Publish to PyPI (requires API token in ~/.pypirc)
twine upload dist/*
```

### PyPI Configuration

**~/.pypirc**:
```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

### GitHub Release

```bash
gh release create v1.0.0 --title "v1.0.0 - ayga-mcp-client" \
  --notes-file release_notes.md \
  dist/ayga_mcp_client-1.0.0-py3-none-any.whl \
  dist/ayga_mcp_client-1.0.0.tar.gz
```

## Testing

Tests run directly (not via pytest CLI to avoid async event loop issues):

```bash
python tests/test_basic.py
```

Or with pytest:
```bash
pytest tests/ -v
```

## Usage Examples

### Claude Desktop

**File**: `~/.config/Claude/claude_desktop_config.json` (Linux/macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

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

**File**: `.vscode/mcp.json`

```json
{
  "servers": {
    "redis-api": {
      "command": "ayga-mcp-client",
      "args": ["--api-key", "YOUR_API_KEY"]
    }
  }
}
```

### Environment Variables

```bash
export REDIS_API_URL="https://redis.ayga.tech"
export REDIS_USERNAME="your_username"
export REDIS_PASSWORD="your_password"
# OR
export REDIS_API_KEY="your_api_key"

ayga-mcp-client
```

## Common Issues & Solutions

### Issue: "Cannot find module 'ayga_mcp_client'"

**Solution**: Install package: `pip install ayga-mcp-client`

### Issue: Authentication fails

**Solutions**:
- Check credentials at https://redis.ayga.tech
- Verify API endpoint: `curl https://redis.ayga.tech/health`
- Check logs: MCP clients usually log stderr to console

### Issue: Tools not appearing in Claude Desktop

**Solutions**:
1. Restart Claude Desktop completely
2. Check config file syntax (valid JSON)
3. Verify command runs: `ayga-mcp-client --help`
4. Check Claude logs: `~/Library/Logs/Claude/` (macOS) or `%APPDATA%\Claude\logs\` (Windows)

## Development Workflow

1. **Clone**: `git clone https://github.com/ozand/ayga-mcp-client.git`
2. **Install dev dependencies**: `pip install -e ".[dev]"`
3. **Make changes**
4. **Run tests**: `pytest`
5. **Build**: `python -m build`
6. **Test locally**: `pip install dist/ayga_mcp_client-*.whl`
7. **Commit & push**
8. **Create release**: `gh release create vX.Y.Z`
9. **Publish to PyPI**: Auto-triggered via GitHub Actions (or manual `twine upload`)

## Related Projects

- **redis_wrapper**: FastAPI backend providing the API (https://github.com/ozand/redis_wrapper)
- **MCP Protocol**: https://modelcontextprotocol.io/
- **A-Parser**: Windows application for web scraping (polls Redis queue)

## Future Enhancements

- [ ] Register in official MCP Registry
- [ ] Add more parser tools (Reddit, Telegram, Translation, etc.)
- [ ] Implement caching for frequently used parsers
- [ ] Add retry logic with exponential backoff
- [ ] Support for batch operations
- [ ] Streaming results for long-running parsers
- [ ] Health check monitoring
- [ ] Metrics and observability

## Contact

- **API Docs**: https://redis.ayga.tech/docs
- **Issues**: https://github.com/ozand/ayga-mcp-client/issues
- **Support**: support@ayga.tech
