"""Basic tests for ayga-mcp-client."""

import pytest
from ayga_mcp_client import create_mcp_server, RedisAPIClient


def test_create_server():
    """Test server creation."""
    server = create_mcp_server(
        api_url="https://redis.ayga.tech",
        username="test",
        password="test",
    )
    assert server is not None
    assert server.name == "ayga-mcp-client"


def test_client_creation():
    """Test API client creation."""
    client = RedisAPIClient(
        base_url="https://redis.ayga.tech",
        username="test",
        password="test",
    )
    assert client.base_url == "https://redis.ayga.tech"
    assert client.username == "test"


@pytest.mark.asyncio
async def test_client_close():
    """Test client cleanup."""
    client = RedisAPIClient()
    await client.close()
    # Should not raise
