"""MCP Server implementation using official MCP SDK."""

import asyncio
import json
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .api.client import RedisAPIClient


# Parser definitions (21 parsers)
PARSERS = [
    {"id": "perplexity", "name": "Perplexity AI", "description": "Search and research with Perplexity AI"},
    {"id": "chatgpt", "name": "ChatGPT", "description": "ChatGPT with web search capabilities"},
    {"id": "claude", "name": "Claude AI", "description": "Anthropic Claude AI assistant"},
    {"id": "gemini", "name": "Google Gemini", "description": "Google Gemini AI model"},
    {"id": "copilot", "name": "Microsoft Copilot", "description": "Microsoft Copilot AI"},
    {"id": "grok", "name": "xAI Grok", "description": "xAI Grok AI assistant"},
    {"id": "deepseek", "name": "DeepSeek", "description": "DeepSeek AI model"},
    {"id": "google", "name": "Google Search", "description": "Google web search"},
    {"id": "bing", "name": "Bing Search", "description": "Bing web search"},
    {"id": "duckduckgo", "name": "DuckDuckGo", "description": "DuckDuckGo search engine"},
    {"id": "youtube_search", "name": "YouTube Search", "description": "Search YouTube videos"},
    {"id": "youtube_video", "name": "YouTube Video Info", "description": "Get YouTube video details"},
    {"id": "reddit_posts", "name": "Reddit Posts", "description": "Search Reddit posts"},
    {"id": "reddit_comments", "name": "Reddit Comments", "description": "Search Reddit comments"},
    {"id": "reddit_post_info", "name": "Reddit Post Info", "description": "Get Reddit post details"},
    {"id": "telegram_group", "name": "Telegram Messages", "description": "Scrape Telegram channel messages"},
    {"id": "bing_translate", "name": "Bing Translator", "description": "Translate text with Bing"},
    {"id": "google_translate", "name": "Google Translate", "description": "Translate text with Google"},
    {"id": "deepl_translate", "name": "DeepL Translator", "description": "Translate text with DeepL"},
    {"id": "yandex_translate", "name": "Yandex Translator", "description": "Translate text with Yandex"},
    {"id": "nethttp", "name": "HTTP Fetcher", "description": "Fetch content from URL"},
]


class RedisMCPServer:
    """MCP Server for Redis API."""
    
    def __init__(self, api_client: RedisAPIClient):
        self.client = api_client
        self.server = Server("redis-mcp-client")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP request handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools."""
            tools = []
            
            # Parser tools
            for parser in PARSERS:
                tools.append(Tool(
                    name=f"search_{parser['id']}",
                    description=parser['description'],
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query or prompt"
                            },
                            "timeout": {
                                "type": "integer",
                                "description": "Maximum wait time in seconds",
                                "default": 90
                            }
                        },
                        "required": ["query"]
                    }
                ))
            
            # Redis tools
            tools.extend([
                Tool(
                    name="redis_get",
                    description="Get a value from Redis by key",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "key": {"type": "string", "description": "Redis key"}
                        },
                        "required": ["key"]
                    }
                ),
                Tool(
                    name="redis_set",
                    description="Set a key-value pair in Redis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "key": {"type": "string", "description": "Redis key"},
                            "value": {"type": "string", "description": "Value to store"},
                            "ttl": {"type": "integer", "description": "TTL in seconds (optional)"}
                        },
                        "required": ["key", "value"]
                    }
                ),
            ])
            
            # Metadata tools
            tools.extend([
                Tool(
                    name="list_parsers",
                    description="List all available AI parsers",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="get_parser_info",
                    description="Get detailed information about a parser",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "parser_id": {"type": "string", "description": "Parser ID"}
                        },
                        "required": ["parser_id"]
                    }
                ),
                Tool(
                    name="health_check",
                    description="Check API health status",
                    inputSchema={"type": "object", "properties": {}}
                ),
            ])
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Execute a tool."""
            try:
                # Parser tools
                if name.startswith("search_"):
                    parser_id = name.replace("search_", "")
                    query = arguments["query"]
                    timeout = arguments.get("timeout", 90)
                    
                    # Submit task
                    task = await self.client.submit_parser_task(parser_id, query)
                    task_id = task.get("task_id")
                    
                    # Wait for result
                    result = await self.client.wait_for_result(task_id, timeout)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2, ensure_ascii=False)
                    )]
                
                # Redis tools
                elif name == "redis_get":
                    value = await self.client.redis_get(arguments["key"])
                    return [TextContent(
                        type="text",
                        text=value or "null"
                    )]
                
                elif name == "redis_set":
                    await self.client.redis_set(
                        arguments["key"],
                        arguments["value"],
                        arguments.get("ttl")
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps({"success": True})
                    )]
                
                # Metadata tools
                elif name == "list_parsers":
                    parsers = await self.client.list_parsers()
                    return [TextContent(
                        type="text",
                        text=json.dumps(parsers, indent=2)
                    )]
                
                elif name == "get_parser_info":
                    info = await self.client.get_parser_info(arguments["parser_id"])
                    return [TextContent(
                        type="text",
                        text=json.dumps(info, indent=2)
                    )]
                
                elif name == "health_check":
                    health = await self.client.health_check()
                    return [TextContent(
                        type="text",
                        text=json.dumps(health, indent=2)
                    )]
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)})
                )]
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def create_server(
    api_url: str | None = None,
    username: str | None = None,
    password: str | None = None,
    api_key: str | None = None,
) -> RedisMCPServer:
    """Create configured MCP server."""
    client = RedisAPIClient(
        base_url=api_url,
        username=username,
        password=password,
        api_key=api_key,
    )
    return RedisMCPServer(client)
