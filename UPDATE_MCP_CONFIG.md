# Update Your VS Code MCP Configuration

**Action Required:** Rename MCP server from `"redis-api"` to `"ayga-mcp-client"` for consistency.

## Location

**Windows:** `%APPDATA%\Code\User\mcp.json`  
**macOS:** `~/Library/Application Support/Code/User/mcp.json`  
**Linux:** `~/.config/Code/User/mcp.json`

## Change Required

### Before (old name):
```json
{
  "servers": {
    "redis-api": {
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

### After (new name):
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

## What Changes

1. Server name: `"redis-api"` → `"ayga-mcp-client"`
2. Usage in chat: `@redis-api` → `@ayga-mcp-client`

## Why This Change?

- Package name is `ayga-mcp-client` (not redis-related)
- Avoids confusion with `redis-mcp-server` (different tool in redis_wrapper)
- Consistent branding across documentation and usage

## Steps

1. Open `%APPDATA%\Code\User\mcp.json` in text editor
2. Find `"redis-api"` key
3. Rename to `"ayga-mcp-client"`
4. Save file
5. Reload VS Code window (Ctrl+Shift+P → "Developer: Reload Window")

## After Reload

Test with:
```
@ayga-mcp-client list_parsers
@ayga-mcp-client get_youtube_suggest query="python"
```

## Full Example mcp.json

```json
{
  "inputs": [...],
  "servers": {
    "git": {...},
    "github": {...},
    "ayga-mcp-client": {
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

## Note

This is just a name change for clarity. The functionality remains identical.
