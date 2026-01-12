# Quick Update to v1.3.0

## Install/Update

```bash
pip install --upgrade ayga-mcp-client
```

## What's New in v1.3.0

- **39 parsers total** (was 29): Added 10 new parsers
- **Content** (2): article_extractor, text_extractor
- **Social expansion** (6): Instagram (5), TikTok (1)
- **Analytics** (1): google_trends
- **Visual** (1): pinterest_search

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

## All Parsers (39 total)

- **FreeAI (6)**: Perplexity, GoogleAI, ChatGPT, Kimi, DeepAI, Copilot
- **YouTube (6)**: Video, Search, Suggest, Channel, Comments
- **Social (10)**: Instagram (5), TikTok (1), Telegram, Reddit (3)
- **Translation (4)**: Google, DeepL, Bing, Yandex
- **Search Engines (8)**: Google, Yandex, Bing, DuckDuckGo, Baidu, Yahoo, Rambler, You
- **Content (2)**: Article extractor, Text extractor
- **Analytics (1)**: Google Trends
- **Visual (1)**: Pinterest
- **Net (1)**: HTTP fetcher

See [CHANGELOG.md](CHANGELOG.md) for full details.
