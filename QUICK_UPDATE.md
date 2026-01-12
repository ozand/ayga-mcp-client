# Quick Update to v1.1.0

## Install/Update

```bash
pip install --upgrade ayga-mcp-client
```

## Short Server Name: `@ayga`

For easier usage, change your config to use short name `@ayga` instead of `@ayga-mcp-client`.

### Automatic Update (Windows)

```powershell
.\scripts\update_mcp_config.ps1
```

### Manual Update

**VS Code** (`%APPDATA%\Code\User\mcp.json`):
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

**Claude Desktop** (Windows: `%APPDATA%\Claude\claude_desktop_config.json`, macOS/Linux: `~/.config/Claude/claude_desktop_config.json`):
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

## New Usage

```
@ayga list_parsers
@ayga search_perplexity query="test"
@ayga translate_google_translate query="Hello" to_language="ru"
```

## What's New

- **21 parsers** (was 11): YouTube (6), Translation (4), Social (4), FreeAI (6), Net (1)
- **Extended parameters**: Languages, pagination, sorting, presets
- **Correct tool prefixes**: `search_*`, `parse_*`, `translate_*`, `get_*`, `scrape_*`, `fetch_*`

See [UPGRADE_v1.1.0.md](UPGRADE_v1.1.0.md) for full details.
