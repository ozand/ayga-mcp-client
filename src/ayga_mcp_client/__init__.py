"""Redis MCP Client - MCP server for Redis API."""

__version__ = "1.3.0"

from .server import create_mcp_server, run_stdio_server
from .api.client import RedisAPIClient

__all__ = [
    "create_mcp_server",
    "run_stdio_server",
    "RedisAPIClient",
]
