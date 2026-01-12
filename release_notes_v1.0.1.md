# v1.0.1 - Critical Fix: Parser Execution 404 Errors

## 🔧 Bug Fixes

### Critical: Fixed Parser Execution
All parser tools (`search_perplexity`, `search_chatgpt`, `search_claude`, etc.) were returning 404 errors. This has been **completely resolved**.

**Root Cause**: The client was using non-existent API endpoints:
- ❌ `POST /parsers/{id}/execute` (doesn't exist)
- ❌ `GET /results/{task_id}` (doesn't exist)

**Solution**: Updated to use the actual redis_wrapper API structure:
- ✅ `POST /structures/list/aparser_redis_api/lpush` (Redis queue submission)
- ✅ `GET /kv/aparser_redis_api:{task_id}` (Redis KV result retrieval)

### Changes in Detail

1. **Task Submission** (`submit_parser_task`)
   - Now uses Redis list LPUSH endpoint
   - Generates UUID task IDs
   - Maps parser IDs to A-Parser format (`perplexity` → `FreeAI::Perplexity`)
   - Formats tasks correctly: `[taskId, parser, preset, query, {}, {}]`

2. **Result Retrieval** (`get_task_result`)
   - Now uses Redis KV endpoint
   - Parses A-Parser result format: `[taskId, status, errorCode, errorMsg, data, ...]`
   - Handles pending/success/error states correctly
   - Returns structured data with proper error handling

## 📦 Installation

```bash
pip install --upgrade ayga-mcp-client
```

## 🔄 Configuration

Update your MCP config to use the published package:

```json
{
  "servers": {
    "ayga-mcp-client": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## ✅ Verification

After updating, test with:

```bash
# Using Claude Desktop or VS Code Copilot MCP tools
search_perplexity(query="test query", timeout=60)
```

Should now return results instead of 404 errors.

## 📚 Links

- **PyPI**: https://pypi.org/project/ayga-mcp-client/1.0.1/
- **Docs**: https://github.com/ozand/ayga-mcp-client
- **API**: https://redis.ayga.tech/docs
