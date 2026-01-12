"""Test authentication with working API key."""

import sys
sys.path.insert(0, 'src')

import asyncio
import json
from ayga_mcp_client.api.client import RedisAPIClient


async def test():
    client = RedisAPIClient(api_key='GnYEheuF3hs_k_GbQgtTy_LFAB2b3GaSx1PA49u_JOg')
    
    print('Step 1: Testing authentication...')
    try:
        await client._get_client()
        print(f'✓ Authentication successful!')
        print(f'  Token: {client._token[:50]}...')
        
    except Exception as e:
        print(f'✗ Authentication failed: {e}')
        await client.close()
        return
    
    print('\nStep 2: Submitting perplexity task...')
    try:
        task = await client.submit_parser_task('perplexity', 'What is AI in 2025?')
        print(f'✓ Task submitted!')
        print(f'  Task ID: {task.get("task_id")}')
        
        print('\nStep 3: Waiting for result (60s timeout)...')
        result = await client.wait_for_result(task['task_id'], timeout=60)
        print(f'✓ Result received!')
        print(f'  Keys: {list(result.keys())}')
        print(f'  Preview: {json.dumps(result, indent=2)[:1000]}...')
        
    except TimeoutError as e:
        print(f'⏱ Timeout: {e}')
    except Exception as e:
        print(f'✗ Error: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()
    
    await client.close()
    print('\n✓ Client closed')


if __name__ == '__main__':
    asyncio.run(test())
