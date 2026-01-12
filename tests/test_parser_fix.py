"""Test the fixed parser execution."""

import sys
sys.path.insert(0, 'src')

import asyncio
import json
from ayga_mcp_client.api.client import RedisAPIClient


async def test():
    client = RedisAPIClient(api_key='GnYEheuF3hs_k_GbQgtTy_LFAB2b3GaSx1PA49u_JOg')
    
    print('Submitting perplexity task...')
    try:
        task = await client.submit_parser_task('perplexity', 'What is Model Context Protocol?')
        print(f'✓ Task submitted: {json.dumps(task, indent=2)}')
        
        task_id = task.get('task_id')
        print(f'\nWaiting for result (task_id: {task_id})...')
        result = await client.wait_for_result(task_id, timeout=60)
        
        print(f'\n✓ Result received!')
        print(f'Data preview: {json.dumps(result, indent=2)[:500]}...')
        
    except TimeoutError as e:
        print(f'⏱ Timeout: {e}')
    except Exception as e:
        print(f'✗ Error: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()
    
    await client.close()


if __name__ == '__main__':
    asyncio.run(test())
