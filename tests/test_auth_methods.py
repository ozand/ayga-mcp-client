"""Test parser execution without auth exchange."""

import sys
sys.path.insert(0, 'src')

import asyncio
import json
from ayga_mcp_client.api.client import RedisAPIClient


async def test():
    # Create client without triggering auth
    client = RedisAPIClient(api_key='GnYEheuF3hs_k_GbQgtTy_LFAB2b3GaSx1PA49u_JOg')
    client._client = await client._get_client()
    
    # Try using API key directly in headers instead of exchange
    client._token = client.api_key  # Use API key as token
    
    print('Testing direct task submission...')
    try:
        task = await client.submit_parser_task('perplexity', 'What is AI?')
        print(f'✓ Task submitted successfully!')
        print(f'Response: {json.dumps(task, indent=2)}')
        
    except Exception as e:
        print(f'✗ Task submission error: {type(e).__name__}')
        print(f'  Message: {e}')
        
        # Try with X-API-Key header instead
        print('\nTrying with X-API-Key header...')
        import httpx
        client2 = httpx.AsyncClient(timeout=120.0)
        
        try:
            import uuid
            task_id = str(uuid.uuid4())
            task_data = [task_id, "FreeAI::Perplexity", "default", "What is AI?", {}, {}]
            
            response = await client2.post(
                "https://redis.ayga.tech/structures/list/aparser_redis_api/lpush",
                json={"value": json.dumps(task_data)},
                headers={"X-API-Key": client.api_key}
            )
            print(f'Status: {response.status_code}')
            print(f'Response: {response.text[:500]}')
            
        except Exception as e2:
            print(f'✗ Alternative method error: {e2}')
        finally:
            await client2.aclose()
    
    await client.close()


if __name__ == '__main__':
    asyncio.run(test())
