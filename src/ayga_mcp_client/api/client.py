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
        """Submit parser task via Redis queue.
        
        Args:
            parser_id: Parser ID (e.g., 'perplexity', 'chatgpt')
            query: Query string
            options: Optional parser options
            
        Returns:
            Dict with 'task_id' key
        """
        import uuid
        import json as stdlib_json
        
        client = await self._get_client()
        
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Map parser_id to A-Parser format (39 parsers: 6 FreeAI + 6 YouTube + 10 Social + 4 Translation + 8 SE + 2 Content + 1 Analytics + 1 Visual + 1 Net)
        parser_map = {
            # FreeAI Category (6)
            "perplexity": "FreeAI::Perplexity",
            "googleai": "FreeAI::GoogleAI",
            "chatgpt": "FreeAI::ChatGPT",
            "kimi": "FreeAI::Kimi",
            "deepai": "FreeAI::DeepAI",
            "copilot": "FreeAI::Copilot",
            
            # YouTube Category (6)
            "youtube_video": "SE::YouTube::Video",
            "youtube_search": "SE::YouTube",
            "youtube_suggest": "SE::YouTube::Suggest",
            "youtube_channel_videos": "JS::Example::Youtube::Channel::Videos",
            "youtube_channel_about": "Net::HTTP",
            "youtube_comments": "JS::Example::Youtube::Comments",
            
            # Social Media Category (10)
            "telegram_group": "Telegram::GroupScraper",
            "reddit_posts": "Reddit::Posts",
            "reddit_post_info": "Reddit::PostInfo",
            "reddit_comments": "Reddit::Comments",
            "instagram_profile": "Social::Instagram::Profile",
            "instagram_post": "Social::Instagram::Post",
            "instagram_tag": "Social::Instagram::Tag",
            "instagram_geo": "Social::Instagram::Geo",
            "instagram_search": "Social::Instagram::Search",
            "tiktok_profile": "Social::TikTok::Profile",
            
            # Translation Category (4)
            "google_translate": "SE::Google::Translate",
            "deepl_translate": "DeepL::Translator",
            "bing_translate": "SE::Bing::Translator",
            "yandex_translate": "SE::Yandex::Translate",
            
            # Search Engine Category (8)
            "google_search": "SE::Google",
            "yandex_search": "SE::Yandex",
            "bing_search": "SE::Bing",
            "duckduckgo_search": "SE::DuckDuckGo",
            "baidu_search": "SE::Baidu",
            "yahoo_search": "SE::Yahoo",
            "rambler_search": "SE::Rambler",
            "you_search": "SE::You",
            
            # Content Category (2)
            "article_extractor": "HTML::ArticleExtractor",
            "text_extractor": "HTML::TextExtractor",
            
            # Analytics Category (1)
            "google_trends": "SE::Google::Trends",
            
            # Visual Content Category (1)
            "pinterest_search": "SE::Pinterest",
            
            # Net Category (1)
            "http": "Net::HTTP",
        }
        
        aparser_name = parser_map.get(parser_id, f"FreeAI::{parser_id.title()}")
        
        # Extract preset and other options
        preset = options.get("preset", "default") if options else "default"
        
        # Build options dict for A-Parser (5th element in task array)
        aparser_options = {}
        if options:
            # Language parameters (for Translation parsers)
            if "from_language" in options:
                aparser_options["fromLanguage"] = options["from_language"]
            if "to_language" in options:
                aparser_options["toLanguage"] = options["to_language"]
            
            # Pagination parameters
            if "pages_count" in options:
                aparser_options["pagesCount"] = options["pages_count"]
            if "max_comments_count" in options:
                aparser_options["maxCommentsCount"] = options["max_comments_count"]
            if "max_empty_posts" in options:
                aparser_options["maxEmptyPosts"] = options["max_empty_posts"]
            
            # YouTube-specific parameters
            if "interface_language" in options:
                aparser_options["interfaceLanguage"] = options["interface_language"]
            if "subtitles_language" in options:
                aparser_options["subtitlesLanguage"] = options["subtitles_language"]
            if "comments_pages" in options:
                aparser_options["commentsPages"] = options["comments_pages"]
            if "sort" in options:
                aparser_options["sort"] = options["sort"]
            
            # Google Trends parameters
            if "category" in options:
                aparser_options["search_category"] = options["category"]
            if "region" in options:
                aparser_options["search_region"] = options["region"]
            if "time_period" in options:
                aparser_options["search_time"] = options["time_period"]
            if "language" in options:
                aparser_options["hl"] = options["language"]
            if "property" in options:
                aparser_options["search_property"] = options["property"]
            if "use_empty_queries" in options:
                aparser_options["use_empty_queries"] = options["use_empty_queries"]
        
        # A-Parser task format: [taskId, parser, preset, query, options, {}]
        task_data = [task_id, aparser_name, preset, query, aparser_options, {}]
        task_json = stdlib_json.dumps(task_data)
        
        # Submit to Redis list via structures API
        queue_key = "aparser_redis_api"
        response = await client.post(
            f"{self.base_url}/structures/list/{queue_key}/lpush",
            json={"value": task_json},
            headers={"Authorization": f"Bearer {self._token}"},
        )
        response.raise_for_status()
        
        return {"task_id": task_id}
    
    async def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task result from Redis KV.
        
        Args:
            task_id: Task ID from submit_parser_task
            
        Returns:
            Parsed result dict if available, None if not ready yet
        """
        import json as stdlib_json
        
        client = await self._get_client()
        result_key = f"aparser_redis_api:{task_id}"
        
        response = await client.get(
            f"{self.base_url}/kv/{result_key}",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        
        if response.status_code == 404:
            # Task not ready yet
            return None
        
        response.raise_for_status()
        
        # Parse result (comes as string value from Redis)
        result_json = response.json()
        if not result_json or "value" not in result_json:
            return None
            
        # Parse value string
        try:
            result_data = stdlib_json.loads(result_json["value"])
            
            # Check if it's A-Parser array format: [taskId, status, errorCode, errorMsg, data, ...]
            if isinstance(result_data, list) and len(result_data) >= 5:
                task_id_ret, status, error_code, error_msg, data, *rest = result_data
                
                # Check for errors
                if error_code:
                    raise ValueError(f"Parser error {error_code}: {error_msg}")
                
                if status != "success":
                    return None  # Still processing
                
                # Return parsed data
                return {"data": data, "task_id": task_id_ret}
            
            # Otherwise, it's already a dict (new API format)
            elif isinstance(result_data, dict):
                # Check for success
                if result_data.get("success") == 1:
                    return {"data": result_data, "task_id": task_id}
                elif result_data.get("error"):
                    raise ValueError(f"Parser error: {result_data.get('error')}")
                else:
                    return None  # Still processing
            
            else:
                raise ValueError(f"Unexpected result format: {type(result_data)}")
            
        except (stdlib_json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse result: {e}")
    
    async def wait_for_result(
        self,
        task_id: str,
        timeout: int = 180,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Dict[str, Any]:
        """Poll for task result with exponential backoff.
        
        Uses progressive polling strategy:
        - Start with 1.5s delay
        - Increase by 20% each poll (exponential backoff)
        - Cap at 5s maximum delay
        - Total timeout default 180s for slow parsers
        
        Args:
            task_id: Task ID from submit_parser_task
            timeout: Maximum wait time in seconds (default: 180)
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dict with parsed result
            
        Raises:
            TimeoutError: If result not ready within timeout
        """
        start = asyncio.get_event_loop().time()
        delay = 1.5  # Start with 1.5s (A-Parser needs time to process)
        max_delay = 5.0  # Cap at 5s between polls
        
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
            
            # Exponential backoff: 1.5s, 1.8s, 2.2s, 2.6s, 3.1s, 3.7s, 4.5s, 5s, 5s...
            await asyncio.sleep(delay)
            delay = min(delay * 1.2, max_delay)
    
    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
