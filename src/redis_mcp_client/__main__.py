"""CLI entrypoint for redis-mcp-client."""

import argparse
import asyncio

from .server import create_server


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="MCP Server for Redis API with 21+ AI parsers"
    )
    parser.add_argument(
        "--api-url",
        help="Redis API URL (default: from REDIS_API_URL env or https://redis.ayga.tech)",
    )
    parser.add_argument(
        "--username",
        help="Username for authentication (or use REDIS_USERNAME env)",
    )
    parser.add_argument(
        "--password",
        help="Password for authentication (or use REDIS_PASSWORD env)",
    )
    parser.add_argument(
        "--api-key",
        help="API key for authentication (or use REDIS_API_KEY env)",
    )
    
    args = parser.parse_args()
    
    # Create and run server
    server = create_server(
        api_url=args.api_url,
        username=args.username,
        password=args.password,
        api_key=args.api_key,
    )
    
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
