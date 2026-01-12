# ayga-mcp-client Examples

This document provides detailed examples of all available tools, their request formats, and response structures.

## Table of Contents

- [AI Chat Parsers](#ai-chat-parsers)
- [Search Engines](#search-engines)
- [Social Media](#social-media)
- [Metadata Tools](#metadata-tools)
- [Error Handling](#error-handling)
- [Real-World Use Cases](#real-world-use-cases)

---

## AI Chat Parsers

### search_perplexity

AI-powered search engine with real-time web access and cited sources.

**Request:**
```json
{
  "query": "What are transformer models in AI?",
  "timeout": 90
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0,
      "time_taken": 12.5
    },
    "answer": "Transformer models are a type of neural network architecture introduced in the 2017 paper 'Attention Is All You Need'. They revolutionized natural language processing by using self-attention mechanisms instead of recurrent layers...",
    "sources": [
      {
        "title": "Attention Is All You Need",
        "url": "https://arxiv.org/abs/1706.03762",
        "snippet": "We propose a new simple network architecture..."
      },
      {
        "title": "The Illustrated Transformer",
        "url": "https://jalammar.github.io/illustrated-transformer/",
        "snippet": "The Transformer – a model that uses attention to boost..."
      }
    ],
    "related": [
      "GPT models",
      "BERT",
      "attention mechanism",
      "encoder-decoder architecture"
    ]
  }
}
```

**Claude Desktop Usage:**
```
@redis-api search_perplexity query="latest developments in quantum computing 2026"
```

---

### search_chatgpt

ChatGPT with web search capabilities.

**Request:**
```json
{
  "query": "Explain quantum computing to a 10 year old",
  "timeout": 60
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "answer": "Imagine regular computers use switches that are either ON (like 1) or OFF (like 0). They're like light switches! But quantum computers are special - they can be ON, OFF, or BOTH at the same time! It's like a coin spinning in the air - is it heads or tails? It's both until it lands! This lets quantum computers solve really hard puzzles much faster than regular computers.",
    "web_results": [
      {
        "title": "What is Quantum Computing? - IBM",
        "snippet": "Quantum computers harness the properties of quantum mechanics..."
      }
    ]
  }
}
```

---

### search_claude

Anthropic Claude AI assistant with reasoning capabilities.

**Request:**
```json
{
  "query": "Compare async/await in Python vs JavaScript",
  "timeout": 90
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "answer": "Both Python and JavaScript use async/await for asynchronous programming, but with key differences:\n\n**Python:**\n- Uses `asyncio` event loop\n- Must explicitly run with `asyncio.run()`\n- `await` only works inside `async def` functions\n- Example: `async def fetch(): result = await get_data()`\n\n**JavaScript:**\n- Built-in event loop in runtime (Node.js/browsers)\n- Top-level await supported in modules\n- Promise-based natively\n- Example: `async function fetch() { const result = await getData(); }`\n\nKey similarity: Both prevent callback hell and make async code readable.",
    "code_examples": [
      "# Python\nasync def main():\n    result = await fetch()\n    return result\n\nasyncio.run(main())",
      "// JavaScript\nasync function main() {\n    const result = await fetch();\n    return result;\n}\nmain();"
    ]
  }
}
```

---

### search_gemini

Google Gemini AI with multimodal capabilities.

**Request:**
```json
{
  "query": "What are the best practices for API design in 2026?",
  "timeout": 90
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "answer": "Modern API design in 2026 follows these best practices:\n\n1. **RESTful principles**: Clear resource naming, proper HTTP methods\n2. **GraphQL for complex queries**: Reduces over-fetching\n3. **API versioning**: Use URL path (/v1/, /v2/) or headers\n4. **Rate limiting**: Protect against abuse\n5. **Comprehensive documentation**: OpenAPI/Swagger specs\n6. **Security**: OAuth 2.0, JWT tokens, HTTPS only\n7. **Error handling**: Consistent error response format\n8. **Pagination**: For large datasets\n9. **Caching**: ETags, Cache-Control headers\n10. **Monitoring**: Track usage, errors, performance"
  }
}
```

---

### search_copilot

Microsoft Copilot with web search integration.

**Request:**
```json
{
  "query": "How to optimize PostgreSQL queries for large datasets?",
  "timeout": 90
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "answer": "Here are key strategies for optimizing PostgreSQL queries on large datasets:\n\n**1. Indexing:**\n- Create indexes on frequently queried columns\n- Use composite indexes for multi-column filters\n- Consider partial indexes for filtered queries\n\n**2. Query Optimization:**\n- Use EXPLAIN ANALYZE to identify bottlenecks\n- Avoid SELECT *; specify needed columns\n- Use JOINs instead of subqueries when possible\n\n**3. Partitioning:**\n- Partition large tables by date/range\n- Enables parallel query execution\n\n**4. Configuration:**\n- Tune shared_buffers (25% of RAM)\n- Adjust work_mem for sorting operations\n- Enable parallel workers\n\n**5. Maintenance:**\n- Regular VACUUM and ANALYZE\n- Update statistics for query planner",
    "code_snippets": [
      "-- Create index\nCREATE INDEX idx_users_email ON users(email);",
      "-- Analyze query\nEXPLAIN ANALYZE SELECT * FROM orders WHERE created_at > '2026-01-01';"
    ]
  }
}
```

---

### search_grok

xAI Grok assistant with real-time data access.

**Request:**
```json
{
  "query": "What's trending on social media today?",
  "timeout": 60
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "answer": "Top trending topics today (Jan 10, 2026):\n\n1. **#AI2026** - Major AI policy announcements\n2. **#SpaceX** - Starship Mars mission updates\n3. **#ClimateAction** - Global renewable energy summit\n4. **#TechEarnings** - Q4 2025 tech company results\n5. **#QuantumLeap** - IBM quantum computer breakthrough",
    "trends": [
      {"topic": "AI2026", "volume": 2500000, "sentiment": "positive"},
      {"topic": "SpaceX", "volume": 1800000, "sentiment": "excited"}
    ]
  }
}
```

---

### search_deepseek

DeepSeek AI assistant specialized in technical queries.

**Request:**
```json
{
  "query": "Explain the difference between TCP and UDP",
  "timeout": 60
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "answer": "**TCP (Transmission Control Protocol):**\n- Connection-oriented (handshake required)\n- Reliable: guarantees packet delivery and order\n- Error checking and retransmission\n- Slower due to overhead\n- Use cases: HTTP, HTTPS, email, file transfers\n\n**UDP (User Datagram Protocol):**\n- Connectionless (no handshake)\n- Unreliable: no delivery guarantee\n- No error correction\n- Faster, lower latency\n- Use cases: streaming, gaming, DNS, VoIP\n\n**When to use:**\n- TCP: When reliability matters (web pages, downloads)\n- UDP: When speed matters (video calls, live streams)",
    "comparison_table": {
      "reliability": {"TCP": "High", "UDP": "Low"},
      "speed": {"TCP": "Slower", "UDP": "Faster"},
      "ordering": {"TCP": "Guaranteed", "UDP": "Not guaranteed"}
    }
  }
}
```

---

## Search Engines

### search_google_search

Google web search with result snippets.

**Request:**
```json
{
  "query": "Python asyncio tutorial",
  "timeout": 30
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "results": [
      {
        "position": 1,
        "title": "Asyncio — Asynchronous I/O — Python 3.13 documentation",
        "url": "https://docs.python.org/3/library/asyncio.html",
        "snippet": "asyncio is a library to write concurrent code using the async/await syntax. asyncio is used as a foundation for multiple Python asynchronous frameworks...",
        "domain": "docs.python.org"
      },
      {
        "position": 2,
        "title": "Getting Started With Async Features in Python",
        "url": "https://realpython.com/async-io-python/",
        "snippet": "Learn how to use Python's asyncio library for concurrent programming. This tutorial covers event loops, coroutines, and best practices...",
        "domain": "realpython.com"
      },
      {
        "position": 3,
        "title": "Python Asyncio Tutorial - YouTube",
        "url": "https://www.youtube.com/watch?v=t5Bo1Je9EmE",
        "snippet": "Complete guide to asynchronous programming in Python...",
        "domain": "youtube.com"
      }
    ],
    "total_results": 1420000,
    "search_time": 0.42
  }
}
```

---

### search_bing_search

Bing web search with rich results.

**Request:**
```json
{
  "query": "FastAPI best practices",
  "timeout": 30
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "results": [
      {
        "title": "FastAPI Best Practices - GitHub",
        "url": "https://github.com/zhanymkanov/fastapi-best-practices",
        "snippet": "A collection of best practices, patterns, and conventions for building FastAPI applications...",
        "date": "2026-01-05"
      },
      {
        "title": "FastAPI Documentation - Best Practices",
        "url": "https://fastapi.tiangolo.com/best-practices/",
        "snippet": "Official guide to structuring FastAPI projects, dependency injection, and async operations..."
      }
    ],
    "related_searches": [
      "FastAPI vs Flask",
      "FastAPI authentication",
      "FastAPI deployment"
    ]
  }
}
```

---

### search_duckduckgo

Privacy-focused search without tracking.

**Request:**
```json
{
  "query": "MCP protocol documentation",
  "timeout": 30
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "results": [
      {
        "title": "Model Context Protocol - Anthropic",
        "url": "https://modelcontextprotocol.io/",
        "snippet": "MCP is an open protocol that enables seamless integration between LLM applications and external data sources..."
      },
      {
        "title": "MCP Specification - GitHub",
        "url": "https://github.com/anthropics/mcp",
        "snippet": "Technical specification and reference implementation of the Model Context Protocol..."
      }
    ],
    "instant_answer": "Model Context Protocol (MCP) is an open standard for connecting AI assistants to data sources and tools."
  }
}
```

---

## Social Media

### search_youtube_search

Search YouTube videos with metadata.

**Request:**
```json
{
  "query": "Docker tutorial for beginners",
  "timeout": 30
}
```

**Response:**
```json
{
  "success": 1,
  "data": {
    "info": {
      "success": 1,
      "retries": 0
    },
    "videos": [
      {
        "title": "Docker Tutorial for Beginners - Full Course in 3 Hours",
        "video_id": "3c-iBn73dDE",
        "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
        "channel": "TechWorld with Nana",
        "channel_url": "https://www.youtube.com/c/TechWorldwithNana",
        "duration": "3:10:24",
        "views": 2500000,
        "published": "2025-11-15",
        "thumbnail": "https://i.ytimg.com/vi/3c-iBn73dDE/maxresdefault.jpg",
        "description": "Complete Docker tutorial covering containers, images, volumes, networks, and Docker Compose..."
      },
      {
        "title": "Learn Docker in 12 Minutes",
        "video_id": "YFl2mCHdv24",
        "url": "https://www.youtube.com/watch?v=YFl2mCHdv24",
        "channel": "Fireship",
        "duration": "12:15",
        "views": 1800000,
        "published": "2025-12-01",
        "description": "Quick introduction to Docker fundamentals..."
      }
    ],
    "total_results": 54000
  }
}
```

---

## Metadata Tools

### list_parsers

Get list of all available parsers with details.

**Request:**
```json
{}
```

**Response:**
```json
{
  "parsers": [
    {
      "id": "perplexity",
      "aparser_name": "FreeAI::Perplexity",
      "name": "Perplexity AI",
      "description": "AI-powered search with cited sources",
      "category": "AI Chat",
      "status": "active",
      "features": ["web_search", "citations", "real_time"]
    },
    {
      "id": "chatgpt",
      "aparser_name": "FreeAI::ChatGPT",
      "name": "ChatGPT",
      "description": "OpenAI ChatGPT with web browsing",
      "category": "AI Chat",
      "status": "active",
      "features": ["conversation", "web_search", "code_generation"]
    },
    {
      "id": "google_search",
      "aparser_name": "Google::Search",
      "name": "Google Search",
      "description": "Google web search engine",
      "category": "Search Engine",
      "status": "active",
      "features": ["web_search", "snippets"]
    }
  ],
  "total": 11,
  "categories": {
    "AI Chat": 7,
    "Search Engine": 3,
    "Social Media": 1
  }
}
```

**Claude Desktop Usage:**
```
@redis-api list_parsers
```

---

### get_parser_info

Get detailed information about specific parser.

**Request:**
```json
{
  "parser_id": "perplexity"
}
```

**Response:**
```json
{
  "id": "perplexity",
  "aparser_name": "FreeAI::Perplexity",
  "name": "Perplexity AI",
  "description": "AI-powered search engine with real-time web access and source citations",
  "category": "AI Chat",
  "status": "active",
  "features": [
    "web_search",
    "source_citations",
    "real_time_data",
    "follow_up_questions"
  ],
  "options": {
    "timeout": {
      "type": "integer",
      "default": 90,
      "min": 30,
      "max": 120,
      "description": "Maximum wait time in seconds"
    },
    "locale": {
      "type": "string",
      "default": "en-US",
      "options": ["en-US", "ru-RU", "de-DE"],
      "description": "Response language"
    }
  },
  "rate_limits": {
    "requests_per_minute": 20,
    "concurrent_requests": 5
  },
  "response_format": {
    "success": "integer (0 or 1)",
    "data": {
      "answer": "string",
      "sources": "array of objects",
      "related": "array of strings"
    },
    "info": {
      "success": "integer",
      "retries": "integer",
      "time_taken": "float"
    }
  }
}
```

---

### health_check

Check API and parsers availability.

**Request:**
```json
{}
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.2",
  "timestamp": "2026-01-10T15:30:45Z",
  "uptime_seconds": 86400,
  "components": {
    "api": {
      "status": "up",
      "response_time_ms": 12
    },
    "redis": {
      "status": "connected",
      "ping_ms": 2
    },
    "aparser": {
      "status": "running",
      "active_tasks": 3,
      "queue_size": 0
    }
  },
  "parsers": {
    "total": 11,
    "active": 11,
    "inactive": 0
  },
  "statistics": {
    "total_requests_today": 1523,
    "success_rate": 98.5,
    "average_response_time_ms": 15400
  }
}
```

---

## Error Handling

### Timeout Error

**Request:**
```json
{
  "query": "Very complex query that takes too long",
  "timeout": 10
}
```

**Response:**
```json
{
  "error": "Task timeout after 10 seconds",
  "task_id": "cb5e8e96-8a7f-4b8c-9d1e-2f3a4b5c6d7e",
  "parser": "perplexity",
  "query": "Very complex query that takes too long",
  "timestamp": "2026-01-10T15:30:45Z"
}
```

---

### Parser Not Found

**Request:**
```json
{
  "parser_id": "unknown_parser"
}
```

**Response:**
```json
{
  "error": "Parser 'unknown_parser' not found",
  "available_parsers": [
    "perplexity",
    "chatgpt",
    "claude",
    "gemini",
    "copilot",
    "grok",
    "deepseek",
    "google_search",
    "bing_search",
    "duckduckgo",
    "youtube_search"
  ],
  "suggestion": "Did you mean 'perplexity'?"
}
```

---

### Authentication Error

**Request:**
```
# Missing or invalid API key
```

**Response:**
```json
{
  "error": "Authentication failed: Invalid API key",
  "status_code": 401,
  "message": "Please provide valid API key via REDIS_API_KEY environment variable",
  "docs": "https://github.com/ozand/ayga-mcp-client#authentication"
}
```

---

### Rate Limit Error

**Response:**
```json
{
  "error": "Rate limit exceeded",
  "status_code": 429,
  "message": "Maximum 20 requests per minute for parser 'perplexity'",
  "retry_after_seconds": 42,
  "current_usage": {
    "requests_this_minute": 20,
    "limit": 20
  }
}
```

---

### Task Execution Error

**Response:**
```json
{
  "success": 0,
  "error_code": 500,
  "error_message": "Parser execution failed: Connection timeout to external service",
  "task_id": "task-uuid-here",
  "parser": "perplexity",
  "info": {
    "retries": 3,
    "last_error": "HTTPConnectionPool timeout"
  }
}
```

---

## Real-World Use Cases

### 1. Research Assistant

Combine multiple parsers for comprehensive research:

```python
import asyncio
from ayga_mcp_client.api.client import RedisAPIClient

async def research_topic(topic: str):
    """Research a topic using multiple AI sources."""
    client = RedisAPIClient(api_key="your_api_key")
    
    # Get different perspectives
    tasks = [
        client.submit_parser_task("perplexity", f"Latest research on {topic}"),
        client.submit_parser_task("chatgpt", f"Explain {topic} in simple terms"),
        client.submit_parser_task("claude", f"Critical analysis of {topic}"),
    ]
    
    # Wait for all results
    task_results = await asyncio.gather(*tasks)
    results = await asyncio.gather(*[
        client.wait_for_result(t['task_id']) 
        for t in task_results
    ])
    
    await client.close()
    return results

# Usage
results = asyncio.run(research_topic("quantum computing"))
```

---

### 2. Content Aggregator

Search multiple sources and compile results:

```python
async def aggregate_content(query: str):
    """Search across multiple platforms."""
    client = RedisAPIClient(api_key="your_api_key")
    
    searches = {
        'google': await client.submit_parser_task("google_search", query),
        'bing': await client.submit_parser_task("bing_search", query),
        'youtube': await client.submit_parser_task("youtube_search", query),
    }
    
    results = {}
    for source, task in searches.items():
        results[source] = await client.wait_for_result(task['task_id'])
    
    await client.close()
    return results
```

---

### 3. Multi-AI Consensus

Get consensus from multiple AI models:

```python
async def get_consensus(question: str):
    """Ask multiple AIs and compare answers."""
    client = RedisAPIClient(api_key="your_api_key")
    
    ais = ["chatgpt", "claude", "gemini", "perplexity"]
    
    tasks = [
        await client.submit_parser_task(ai, question)
        for ai in ais
    ]
    
    answers = await asyncio.gather(*[
        client.wait_for_result(t['task_id'])
        for t in tasks
    ])
    
    await client.close()
    
    # Compare and analyze
    return {
        ai: answer['data'].get('answer', '')
        for ai, answer in zip(ais, answers)
    }
```

---

### 4. Monitoring & Health Check

Monitor API health before critical operations:

```python
async def safe_query(parser: str, query: str):
    """Query with health check first."""
    client = RedisAPIClient(api_key="your_api_key")
    
    # Check health
    health_task = await client.submit_parser_task("health_check", "")
    health = await client.wait_for_result(health_task['task_id'])
    
    if health.get('status') != 'healthy':
        raise RuntimeError("API is not healthy")
    
    # Proceed with query
    task = await client.submit_parser_task(parser, query)
    result = await client.wait_for_result(task['task_id'])
    
    await client.close()
    return result
```

---

## Tips & Best Practices

### 1. Timeout Selection

- **Quick queries** (search engines): 30 seconds
- **AI chat** (simple questions): 60 seconds  
- **Complex AI tasks** (research, analysis): 90-120 seconds

### 2. Error Handling

Always wrap calls in try-except:

```python
try:
    result = await client.wait_for_result(task_id, timeout=90)
except asyncio.TimeoutError:
    print("Task timed out, try increasing timeout")
except Exception as e:
    print(f"Error: {e}")
```

### 3. Parallel Execution

Use `asyncio.gather()` for multiple independent queries:

```python
results = await asyncio.gather(
    client.submit_parser_task("perplexity", "query1"),
    client.submit_parser_task("chatgpt", "query2"),
    client.submit_parser_task("google_search", "query3"),
)
```

### 4. Resource Cleanup

Always close the client:

```python
try:
    # Your operations
    pass
finally:
    await client.close()
```

---

## See Also

- [README.md](README.md) - Installation and setup
- [DEVELOPMENT.md](DEVELOPMENT.md) - Technical architecture
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [API Documentation](https://redis.ayga.tech/docs) - Backend API reference
