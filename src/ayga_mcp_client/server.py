"""MCP server implementation."""

import json
import sys
from typing import Any, Dict, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

from .api.client import RedisAPIClient
from .error_handler import ErrorHandler, create_timeout_error, create_rate_limit_error


# Parser timeout categories based on A-Parser processing time
PARSER_TIMEOUT_CATEGORIES = {
    # Fast parsers (10-30 seconds)
    "fast": {
        "default": 60,
        "parsers": ["perplexity", "chatgpt", "deepai", "kimi", "copilot",
                    "youtube_suggest", "reddit_posts", "reddit_post_info", "reddit_comments",
                    "text_extractor", "http"]
    },
    # Medium parsers (30-60 seconds)
    "medium": {
        "default": 120,
        "parsers": ["youtube_search", "youtube_video", "youtube_channel_videos",
                    "youtube_channel_about", "pinterest_search", "article_extractor",
                    "link_extractor"]
    },
    # Slow parsers (60-120+ seconds)
    "slow": {
        "default": 180,
        "parsers": ["googleai", "google_search", "google_translate", "google_trends",
                    "deepl_translate", "bing_translate", "yandex_translate",
                    "bing_search", "yandex_search", "duckduckgo_search", "baidu_search",
                    "yahoo_search", "rambler_search", "you_search",
                    "youtube_comments", "telegram_group",
                    "instagram_profile", "instagram_post", "instagram_tag",
                    "instagram_geo", "instagram_search", "tiktok_profile"]
    }
}


def get_default_timeout(parser_id: str) -> int:
    """Get default timeout for a parser based on its category."""
    for category, config in PARSER_TIMEOUT_CATEGORIES.items():
        if parser_id in config["parsers"]:
            return config["default"]
    return 120  # Default for unknown parsers


def get_parser_input_schema(parser: Dict[str, Any]) -> Dict[str, Any]:
    """Generate input schema based on parser category."""
    parser_id = parser['id']
    default_timeout = get_default_timeout(parser_id)
    
    # Base schema (all parsers)
    schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Query string, URL, or prompt"
            },
            "timeout": {
                "type": "integer",
                "description": "Maximum wait time in seconds",
                "default": default_timeout
            },
            "preset": {
                "type": "string",
                "description": "Parser preset",
                "default": "default"
            }
        },
        "required": ["query"]
    }
    
    # YouTube parsers - add extended parameters
    if parser_id.startswith("youtube_"):
        if parser_id == "youtube_video":
            schema["properties"]["interface_language"] = {
                "type": "string",
                "description": "Interface language (e.g., 'en', 'ru')",
                "default": "en"
            }
            schema["properties"]["subtitles_language"] = {
                "type": "string",
                "description": "Subtitles language (e.g., 'en', 'ru')",
                "default": "en"
            }
            schema["properties"]["comments_pages"] = {
                "type": "integer",
                "description": "Number of comment pages to fetch (0-20)",
                "default": 0
            }
        elif parser_id == "youtube_search":
            schema["properties"]["pages_count"] = {
                "type": "integer",
                "description": "Number of pages to fetch",
                "default": 1
            }
            schema["properties"]["sort"] = {
                "type": "string",
                "description": "Sort order (relevance, date, viewCount, rating)",
                "default": "relevance"
            }
    
    # Translation parsers - add language parameters
    elif parser_id.endswith("_translate"):
        schema["properties"]["from_language"] = {
            "type": "string",
            "description": "Source language (auto for auto-detection)",
            "default": "auto"
        }
        schema["properties"]["to_language"] = {
            "type": "string",
            "description": "Target language",
            "default": "en"
        }
    
    # Social parsers - add pagination/sorting
    elif parser_id.startswith("reddit_"):
        if parser_id in ["reddit_posts", "reddit_comments"]:
            schema["properties"]["pages_count"] = {
                "type": "integer",
                "description": "Number of pages to fetch",
                "default": 1
            }
            schema["properties"]["sort"] = {
                "type": "string",
                "description": "Sort order",
                "default": "relevance"
            }
        elif parser_id == "reddit_post_info":
            schema["properties"]["max_comments_count"] = {
                "type": "integer",
                "description": "Maximum comments to fetch (0-1000)",
                "default": 100
            }
    elif parser_id == "telegram_group":
        schema["properties"]["max_empty_posts"] = {
            "type": "integer",
            "description": "Max empty posts before stopping",
            "default": 100
        }
    
    # Google Trends - add category, region, time period parameters
    elif parser_id == "google_trends":
        schema["properties"]["category"] = {
            "type": "string",
            "description": "Category ID: 0=All, 3=Arts, 5=Computers, 7=Finance, 12=Business, 13=Health, 16=News, 22=Shopping, 174=Sports",
            "default": "0"
        }
        schema["properties"]["region"] = {
            "type": "string", 
            "description": "Country code (ISO 3166-1): '' (Worldwide), US, GB, DE, FR, RU, JP, CN, etc.",
            "default": ""
        }
        schema["properties"]["time_period"] = {
            "type": "string",
            "description": "Time period: 'today 5-y', 'today 12-m', 'today 3-m', 'today 1-m', 'now 7-d', 'now 1-d', 'now 1-H'",
            "default": "today 5-y"
        }
        schema["properties"]["language"] = {
            "type": "string",
            "description": "Interface language code: en, ru, de, fr, es, ja, etc.",
            "default": "en"
        }
        schema["properties"]["property"] = {
            "type": "string",
            "description": "Search property: '' (Web), 'images', 'news', 'froogle' (Shopping), 'youtube'",
            "default": ""
        }
        schema["properties"]["use_empty_queries"] = {
            "type": "boolean",
            "description": "Get category trending without keywords (query should be language code)",
            "default": False
        }
    
    # Link Extractor - add preset enum
    elif parser_id == "link_extractor":
        schema["properties"]["preset"]["enum"] = ["default", "deep_crawl", "all_links"]
        schema["properties"]["preset"]["description"] = "Preset: 'default' (single page, internal only), 'deep_crawl' (multi-level crawl), 'all_links' (internal + external)"
    
    return schema


# Complete parser list (21 parsers) - synced with redis_wrapper
PARSERS = [
    # FreeAI Category (6 parsers)
    {"id": "perplexity", "name": "Perplexity AI", "description": "AI-powered search with sources", "prefix": "search_"},
    {"id": "googleai", "name": "Google AI", "description": "Google AI-powered search with structured sources", "prefix": "search_"},
    {"id": "chatgpt", "name": "ChatGPT", "description": "ChatGPT with web search", "prefix": "search_"},
    {"id": "kimi", "name": "Kimi AI", "description": "Kimi AI for translation and education", "prefix": "search_"},
    {"id": "deepai", "name": "DeepAI", "description": "DeepAI multi-style chat", "prefix": "search_"},
    {"id": "copilot", "name": "Microsoft Copilot", "description": "Microsoft Copilot search", "prefix": "search_"},
    
    # YouTube Category (6 parsers)
    {"id": "youtube_video", "name": "YouTube Video", "description": "Parse video metadata, subtitles, comments", "prefix": "parse_"},
    {"id": "youtube_search", "name": "YouTube Search", "description": "Search YouTube videos", "prefix": "search_"},
    {"id": "youtube_suggest", "name": "YouTube Suggest", "description": "Get keyword suggestions", "prefix": "get_"},
    {"id": "youtube_channel_videos", "name": "YouTube Channel Videos", "description": "List channel videos", "prefix": "get_"},
    {"id": "youtube_channel_about", "name": "YouTube Channel About", "description": "Get channel info", "prefix": "get_"},
    {"id": "youtube_comments", "name": "YouTube Comments", "description": "Parse video comments", "prefix": "parse_"},
    
    # Social Media Category (10 parsers)
    {"id": "telegram_group", "name": "Telegram Group", "description": "Scrape public group messages", "prefix": "scrape_"},
    {"id": "reddit_posts", "name": "Reddit Posts", "description": "Search Reddit posts", "prefix": "search_"},
    {"id": "reddit_post_info", "name": "Reddit Post Info", "description": "Get post with comments", "prefix": "get_"},
    {"id": "reddit_comments", "name": "Reddit Comments", "description": "Search Reddit comments", "prefix": "search_"},
    {"id": "instagram_profile", "name": "Instagram Profile", "description": "Parse Instagram profile data, posts, followers", "prefix": "parse_"},
    {"id": "instagram_post", "name": "Instagram Post", "description": "Parse Instagram post with likes, comments, caption", "prefix": "parse_"},
    {"id": "instagram_tag", "name": "Instagram Tag", "description": "Parse Instagram posts by hashtag", "prefix": "parse_"},
    {"id": "instagram_geo", "name": "Instagram Geo", "description": "Parse Instagram posts by location", "prefix": "parse_"},
    {"id": "instagram_search", "name": "Instagram Search", "description": "Search Instagram profiles, hashtags, locations", "prefix": "search_"},
    {"id": "tiktok_profile", "name": "TikTok Profile", "description": "Parse TikTok profile data, videos, followers", "prefix": "parse_"},
    
    # Translation Category (4 parsers)
    {"id": "google_translate", "name": "Google Translate", "description": "Google translation service", "prefix": "translate_"},
    {"id": "deepl_translate", "name": "DeepL Translate", "description": "High-quality DeepL translation", "prefix": "translate_"},
    {"id": "bing_translate", "name": "Bing Translate", "description": "Microsoft Bing translator", "prefix": "translate_"},
    {"id": "yandex_translate", "name": "Yandex Translate", "description": "Yandex translator with captcha bypass", "prefix": "translate_"},
    
    # Search Engine Category (8 parsers)
    {"id": "google_search", "name": "Google Search", "description": "Parse Google search results with operators support", "prefix": "search_"},
    {"id": "yandex_search", "name": "Yandex Search", "description": "Parse Yandex search results (Russian search engine)", "prefix": "search_"},
    {"id": "bing_search", "name": "Bing Search", "description": "Parse Bing search results with operators support", "prefix": "search_"},
    {"id": "duckduckgo_search", "name": "DuckDuckGo Search", "description": "Privacy-focused search engine results", "prefix": "search_"},
    {"id": "baidu_search", "name": "Baidu Search", "description": "Parse Chinese search engine Baidu results", "prefix": "search_"},
    {"id": "yahoo_search", "name": "Yahoo Search", "description": "Parse Yahoo search results", "prefix": "search_"},
    {"id": "rambler_search", "name": "Rambler Search", "description": "Parse Russian search engine Rambler results", "prefix": "search_"},
    {"id": "you_search", "name": "You.com Search", "description": "Parse You.com AI-powered search results", "prefix": "search_"},
    
    # Content Category (3 parsers)
    {"id": "article_extractor", "name": "Article Extractor", "description": "Extract articles using Mozilla Readability algorithm", "prefix": "parse_"},
    {"id": "text_extractor", "name": "Text Extractor", "description": "Parse text blocks from web pages with HTML cleaning", "prefix": "parse_"},
    {"id": "link_extractor", "name": "Link Extractor", "description": "Extract all links from HTML pages with filtering and deduplication", "prefix": "extract_"},
    
    # Analytics Category (1 parser)
    {"id": "google_trends", "name": "Google Trends", "description": "Parse trending keywords and interest data from Google Trends", "prefix": "get_"},
    
    # Visual Content Category (1 parser)
    {"id": "pinterest_search", "name": "Pinterest Search", "description": "Parse Pinterest search results: images, titles, descriptions", "prefix": "search_"},
    
    # Net Category (1 parser)
    {"id": "http", "name": "HTTP Fetcher", "description": "Fetch raw URL content", "prefix": "fetch_"},
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
            tool_name = f"{parser['prefix']}{parser['id']}"
            default_timeout = get_default_timeout(parser['id'])
            tools.append(Tool(
                name=tool_name,
                description=f"{parser['description']}. Args: query (string), timeout (int, default {default_timeout})",
                inputSchema=get_parser_input_schema(parser)
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
        
        # Parser tool - match by checking if name matches any parser pattern
        parser = None
        for p in PARSERS:
            tool_name = f"{p['prefix']}{p['id']}"
            if name == tool_name:
                parser = p
                break
        
        if parser:
            parser_id = parser['id']
            query = arguments.get("query")
            default_timeout = get_default_timeout(parser_id)
            timeout = arguments.get("timeout", default_timeout)
            
            if not query:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "query is required"})
                )]
            
            # Collect all optional parameters for A-Parser
            options = {}
            for key in ["preset", "from_language", "to_language", "pages_count", 
                       "max_comments_count", "max_empty_posts", "interface_language",
                       "subtitles_language", "comments_pages", "sort"]:
                if key in arguments:
                    options[key] = arguments[key]
            
            try:
                # Submit task with options
                task = await client.submit_parser_task(parser_id, query, options if options else None)
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
