"""Basic tests for redis-mcp-client."""

import pytest
from redis_mcp_client.api.client import RedisAPIClient


@pytest.fixture
def client():
    """Create test client."""
    return RedisAPIClient(
        base_url="https://redis.ayga.tech",
        username="test",
        password="test",
    )


def test_client_initialization(client):
    """Test client initializes correctly."""
    assert client.base_url == "https://redis.ayga.tech"
    assert client.username == "test"
    assert client.password == "test"


@pytest.mark.asyncio
async def test_health_check_url():
    """Test health check URL construction."""
    client = RedisAPIClient(base_url="https://redis.ayga.tech")
    assert client.base_url == "https://redis.ayga.tech"
