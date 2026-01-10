"""CLI entrypoint for ayga-mcp-client."""

import os
import argparse
import asyncio

from .server import run_stdio_server


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MCP Server for Redis API with 21+ AI parsers"
    )
    parser.add_argument(
        "--api-url",
        default=os.environ.get("REDIS_API_URL", "https://redis.ayga.tech"),
        help="Redis API URL (default: https://redis.ayga.tech)",
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("REDIS_USERNAME"),
        help="Username for authentication",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("REDIS_PASSWORD"),
        help="Password for authentication",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("REDIS_API_KEY"),
        help="API key for authentication (alternative to username/password)",
    )
    
    args = parser.parse_args()
    
    # Run MCP server
    asyncio.run(run_stdio_server(
        api_url=args.api_url,
        username=args.username,
        password=args.password,
        api_key=args.api_key,
    ))


if __name__ == "__main__":
    main()
