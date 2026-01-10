"""HTTP client for Redis API."""

import asyncio
import httpx
from typing import Callable, Optional, Dict, Any


class RedisAPIClient:
    """Client for redis.ayga.tech API."""
    
    def __init__(
        self,
        base_url: str = "https://redis.ayga.tech",
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.api_key = api_key
        self._token: Optional[str] = None
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with auth."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=120.0)
            
            # Authenticate if credentials provided
            if self.username and self.password:
                await self._login()
            elif self.api_key:
                await self._exchange_api_key()
        
        return self._client
    
    async def _login(self):
        """Login with username/password."""
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
    
    async def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        client = await self._get_client()
        response = await client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    async def list_parsers(self) -> Dict[str, Any]:
        """Get list of available parsers."""
        client = await self._get_client()
        response = await client.get(
            f"{self.base_url}/parsers",
            headers={"Authorization": f"Bearer {self._token}"} if self._token else {},
        )
        response.raise_for_status()
        return response.json()
    
    async def get_parser_info(self, parser_id: str) -> Dict[str, Any]:
        """Get parser details."""
        client = await self._get_client()
        response = await client.get(
            f"{self.base_url}/parsers/{parser_id}",
            headers={"Authorization": f"Bearer {self._token}"} if self._token else {},
        )
        response.raise_for_status()
        return response.json()
    
    async def submit_parser_task(self, parser_id: str, query: str, options: Optional[Dict] = None) -> Dict[str, Any]:
        """Submit parser task."""
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
    
    async def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task result if ready."""
        client = await self._get_client()
        response = await client.get(
            f"{self.base_url}/results/{task_id}",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
    
    async def wait_for_result(
        self,
        task_id: str,
        timeout: int = 90,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Dict[str, Any]:
        """Poll for task result with progressive backoff."""
        start = asyncio.get_event_loop().time()
        delay = 1.0
        
        while True:
            elapsed = asyncio.get_event_loop().time() - start
            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} timed out after {timeout}s")
            
            result = await self.get_task_result(task_id)
            
            if result:
                return result
            
            # Report progress
            if progress_callback:
                progress_callback(min(elapsed / timeout, 0.95))
            
            # Progressive backoff: 1s, 1.5s, 2s, 2.5s, max 3s
            await asyncio.sleep(delay)
            delay = min(delay * 1.2, 3.0)
    
    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
