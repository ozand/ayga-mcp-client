"""HTTP client for Redis API."""

import asyncio
import os
from typing import Callable

import httpx


class RedisAPIClient:
    """Client for redis.ayga.tech API."""
    
    def __init__(
        self,
        base_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
    ):
        self.base_url = (base_url or os.environ.get("REDIS_API_URL", "https://redis.ayga.tech")).rstrip("/")
        self.username = username or os.environ.get("REDIS_USERNAME")
        self.password = password or os.environ.get("REDIS_PASSWORD")
        self.api_key = api_key or os.environ.get("REDIS_API_KEY")
        self._token: str | None = None
        self._client: httpx.AsyncClient | None = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with auth."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=120.0)
            
            if self.username and self.password:
                await self._login()
            elif self.api_key:
                await self._exchange_api_key()
        
        return self._client
    
    async def _login(self):
        """Login with username/password to get JWT token."""
        response = await self._client.post(
            f"{self.base_url}/auth/login",
            json={"username": self.username, "password": self.password},
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
    
    async def _exchange_api_key(self):
        """Exchange API key for JWT token."""
        response = await self._client.post(
            f"{self.base_url}/auth/exchange",
            headers={"X-API-Key": self.api_key},
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
    
    async def health_check(self) -> dict:
        """Check API health."""
        client = await self._get_client()
        response = await client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    async def list_parsers(self) -> list[dict]:
        """List all available parsers."""
        client = await self._get_client()
        response = await client.get(
            f"{self.base_url}/parsers",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        response.raise_for_status()
        return response.json()["parsers"]
    
    async def get_parser_info(self, parser_id: str) -> dict:
        """Get parser details."""
        client = await self._get_client()
        response = await client.get(
            f"{self.base_url}/parsers/{parser_id}",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        response.raise_for_status()
        return response.json()
    
    async def submit_parser_task(self, parser_id: str, query: str, options: dict | None = None) -> dict:
        """Submit parser task and return task info."""
        client = await self._get_client()
        payload = {"query": query}
        if options:
            payload["options"] = options
        
        response = await client.post(
            f"{self.base_url}/parsers/{parser_id}/execute",
            json=payload,
            headers={"Authorization": f"Bearer {self._token}"},
        )
        response.raise_for_status()
        return response.json()
    
    async def get_task_result(self, task_id: str) -> dict | None:
        """Get task result if ready, None if pending."""
        client = await self._get_client()
        response = await client.get(
            f"{self.base_url}/results/{task_id}",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 202:
            return None
        else:
            response.raise_for_status()
    
    async def wait_for_result(
        self,
        task_id: str,
        timeout: int = 90,
        progress_callback: Callable[[float], None] | None = None,
    ) -> dict:
        """Poll for task result with progressive backoff."""
        start = asyncio.get_event_loop().time()
        delay = 1.0
        
        while True:
            elapsed = asyncio.get_event_loop().time() - start
            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} timed out after {timeout}s")
            
            result = await self.get_task_result(task_id)
            
            if result is not None:
                return result
            
            if progress_callback:
                progress_callback(min(elapsed / timeout, 0.95))
            
            await asyncio.sleep(delay)
            delay = min(delay * 1.2, 3.0)
    
    async def redis_get(self, key: str) -> str | None:
        """Get value from Redis."""
        client = await self._get_client()
        response = await client.get(
            f"{self.base_url}/kv/{key}",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        
        if response.status_code == 200:
            return response.json()["value"]
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
    
    async def redis_set(self, key: str, value: str, ttl: int | None = None) -> bool:
        """Set value in Redis."""
        client = await self._get_client()
        payload = {"key": key, "value": value}
        if ttl:
            payload["ttl"] = ttl
        
        response = await client.post(
            f"{self.base_url}/kv",
            json=payload,
            headers={"Authorization": f"Bearer {self._token}"},
        )
        response.raise_for_status()
        return True
    
    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
