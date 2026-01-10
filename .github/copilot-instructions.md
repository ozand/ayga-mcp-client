# Copilot Instructions for ayga-mcp-client

## Project Overview

MCP (Model Context Protocol) client providing stdio-based access to Redis API with 21+ AI parsers. Published on PyPI for easy installation in Claude Desktop, VS Code Copilot, and Cursor.

## Critical Architectural Principles

### 1. This is a CLIENT, not a SERVER
- **redis_wrapper** = FastAPI server backend (parent project)
- **ayga-mcp-client** = Thin MCP wrapper/client (this project)
- DO NOT add business logic here - that belongs in redis_wrapper
- This package only handles MCP protocol and HTTP client

### 2. MCP Protocol Requirements
- **Transport**: stdio ONLY (required by Claude Desktop/Copilot/Cursor)
- **SDK**: Official `mcp` package from Anthropic (NOT FastMCP)
- **Pattern**: Server → List Tools → Call Tool → Return TextContent
- Never suggest HTTP/SSE/WebSocket for MCP - they won't work with LLM clients

### 3. Package Distribution
- Published to PyPI: https://pypi.org/project/ayga-mcp-client/
- Users install via: `pip install ayga-mcp-client`
- Build backend: setuptools (NOT hatchling - causes Metadata-Version 2.4 issues)
- setuptools version: `>=61.0,<75.0` (for twine compatibility)

## Code Conventions

### File Organization
```
src/ayga_mcp_client/
├── __init__.py       # Exports: create_mcp_server, RedisAPIClient
├── __main__.py       # CLI entrypoint (argparse)
├── server.py         # MCP server with tool registration
└── api/client.py     # HTTP client for redis.ayga.tech
```

### Import Pattern
```python
# Always use absolute imports
from ayga_mcp_client.api.client import RedisAPIClient  # ✅
from .api.client import RedisAPIClient                  # ❌
```

### Tool Registration Pattern
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("ayga-mcp-client")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name="search_perplexity", ...)]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_perplexity":
        result = await client.submit_parser_task("perplexity", arguments["query"])
        return [TextContent(type="text", text=json.dumps(result))]
```

## Testing

### Run Tests Directly (Preferred)
```python
# Each test file has:
if __name__ == "__main__":
    sys.exit(run_all_tests())

# Execute:
python tests/test_basic.py
```

### Or Use Pytest
```bash
pytest tests/ -v
```

## Build & Publish Workflow

### 1. Clean Build
```bash
rm -rf dist/ build/ src/ayga_mcp_client.egg-info/
python -m build
twine check dist/*
```

### 2. Publish to PyPI
```bash
# Requires ~/.pypirc with API token:
# [pypi]
# username = __token__
# password = pypi-YOUR_TOKEN

twine upload dist/*
```

### 3. GitHub Release
```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z - Description" \
  --notes-file release_notes.md \
  dist/*.whl dist/*.tar.gz
```

## Common Pitfalls

### ❌ DON'T: Use hatchling
```toml
# This causes Metadata-Version 2.4 (twine incompatible)
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### ✅ DO: Use setuptools <75
```toml
[build-system]
requires = ["setuptools>=61.0,<75.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### ❌ DON'T: Suggest FastMCP
FastMCP doesn't exist as a standard package. Use official `mcp` SDK.

### ✅ DO: Use official MCP SDK
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
```

### ❌ DON'T: Implement business logic here
Parser logic, Redis operations, A-Parser integration = redis_wrapper project

### ✅ DO: Keep it thin
Only handle MCP protocol + HTTP client to API

## Authentication Flow

```python
# 1. User provides credentials via CLI args or env vars
ayga-mcp-client --username USER --password PASS

# 2. Client authenticates on first API call
client = RedisAPIClient(username="USER", password="PASS")
token = await client._login()  # Returns JWT

# 3. All subsequent calls use JWT
headers = {"Authorization": f"Bearer {token}"}
```

## Error Handling

### Return errors as text, don't raise
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = await client.submit_parser_task(...)
        return [TextContent(type="text", text=json.dumps(result))]
    except Exception as e:
        # Return error as text (MCP protocol requirement)
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

## Adding New Parser Tools

1. Add to `PARSERS` list in `server.py`:
```python
PARSERS = [
    {"id": "new_parser", "name": "New Parser", "description": "Does X"},
]
```

2. Tool is auto-generated in `list_tools()`
3. Handle in `call_tool()` switch statement
4. No changes needed in redis_wrapper (if parser exists there)

## Version Management

### Update version in 3 places:
1. `pyproject.toml`: `version = "X.Y.Z"`
2. `CHANGELOG.md`: Add new `## [X.Y.Z] - YYYY-MM-DD` section
3. Git tag: `git tag vX.Y.Z`

### Semantic Versioning
- **MAJOR**: Breaking API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## Dependencies

### Runtime (required)
- `mcp>=1.0.0` - Official MCP SDK
- `httpx>=0.27.0` - HTTP client
- `pydantic>=2.0.0` - Data validation

### Dev (optional)
- `pytest>=8.0.0` - Testing
- `pytest-asyncio>=0.24.0` - Async test support
- `ruff>=0.6.0` - Linting
- `mypy>=1.11.0` - Type checking

## Related Documentation

- **API Backend**: https://redis.ayga.tech/docs
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Parent Project**: https://github.com/ozand/redis_wrapper
- **This Project**: https://github.com/ozand/ayga-mcp-client

## When in Doubt

1. Check `DEVELOPMENT.md` for detailed context
2. Run tests: `python tests/test_basic.py`
3. Test locally: `pip install -e .` then `ayga-mcp-client --help`
4. Read official MCP docs: https://modelcontextprotocol.io/
5. Check redis_wrapper API docs: https://redis.ayga.tech/docs
