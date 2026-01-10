"""MCP server implementation."""

import json
import sys
from typing import Any, Dict, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

from .api.client import RedisAPIClient


# Parser list - будет загружаться из API
PARSERS = [
    {"id": "perplexity", "name": "Perplexity AI", "description": "AI-powered search with sources"},
    {"id": "chatgpt", "name": "ChatGPT", "description": "ChatGPT with web search"},
    {"id": "claude", "name": "Claude AI", "description": "Anthropic Claude assistant"},
    {"id": "gemini", "name": "Google Gemini", "description": "Google Gemini AI"},
    {"id": "copilot", "name": "Microsoft Copilot", "description": "Microsoft Copilot search"},
    {"id": "grok", "name": "Grok AI", "description": "xAI Grok assistant"},
    {"id": "deepseek", "name": "DeepSeek", "description": "DeepSeek AI assistant"},
    {"id": "google_search", "name": "Google Search", "description": "Google web search"},
    {"id": "bing_search", "name": "Bing Search", "description": "Bing web search"},
    {"id": "duckduckgo", "name": "DuckDuckGo", "description": "DuckDuckGo search"},
    {"id": "youtube_search", "name": "YouTube Search", "description": "Search YouTube videos"},
]


def create_mcp_server(
    api_url: str = "https://redis.ayga.tech",
    username: Optional[str] = None,
    password: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Server:
    """Create MCP server with Redis API integration."""
    
    server = Server("ayga-mcp-client")
    client = RedisAPIClient(
        base_url=api_url,
        username=username,
        password=password,
        api_key=api_key,
    )
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        tools = []
        
        # Add parser tools
        for parser in PARSERS:
            tools.append(Tool(
                name=f"search_{parser['id']}",
                description=f"{parser['description']}. Args: query (string), timeout (int, default 90)",
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
        
        # Add metadata tools
        tools.extend([
            Tool(
                name="list_parsers",
                description="List all available parsers with details",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="get_parser_info",
                description="Get detailed information about a specific parser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "parser_id": {
                            "type": "string",
                            "description": "Parser identifier (e.g., 'perplexity', 'chatgpt')"
                        }
                    },
                    "required": ["parser_id"]
                }
            ),
            Tool(
                name="health_check",
                description="Check Redis API health status",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
        ])
        
        return tools
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
        """Handle tool calls."""
        
        # Health check
        if name == "health_check":
            result = await client.health_check()
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        # List parsers
        if name == "list_parsers":
            result = await client.list_parsers()
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        # Get parser info
        if name == "get_parser_info":
            parser_id = arguments.get("parser_id")
            if not parser_id:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "parser_id is required"})
                )]
            
            result = await client.get_parser_info(parser_id)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        # Parser tool
        if name.startswith("search_"):
            parser_id = name[7:]  # Remove 'search_' prefix
            query = arguments.get("query")
            timeout = arguments.get("timeout", 90)
            
            if not query:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "query is required"})
                )]
            
            try:
                # Submit task
                task = await client.submit_parser_task(parser_id, query)
                task_id = task.get("task_id")
                
                # Wait for result
                result = await client.wait_for_result(task_id, timeout=timeout)
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            except TimeoutError as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)})
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Failed to execute parser: {str(e)}"})
                )]
        
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"})
        )]
    
    return server


async def run_stdio_server(
    api_url: str = "https://redis.ayga.tech",
    username: Optional[str] = None,
    password: Optional[str] = None,
    api_key: Optional[str] = None,
):
    """Run MCP server with stdio transport."""
    server = create_mcp_server(api_url, username, password, api_key)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
