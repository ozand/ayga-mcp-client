"""Debug result retrieval."""

import sys
sys.path.insert(0, 'src')

import asyncio
import json
from ayga_mcp_client.api.client import RedisAPIClient


async def test():
    client = RedisAPIClient(api_key='GnYEheuF3hs_k_GbQgtTy_LFAB2b3GaSx1PA49u_JOg')
    
    # Authenticate
    await client._get_client()
    print(f'✓ Authenticated')
    
    # Submit task
    task = await client.submit_parser_task('perplexity', 'What is AI?')
    task_id = task['task_id']
    print(f'✓ Task ID: {task_id}')
    
    # Manual check with detailed logging
    import httpx
    result_key = f"aparser_redis_api:{task_id}"
    
    for i in range(10):
        print(f'\n[Attempt {i+1}/10] Checking {result_key}...')
        
        response = await client._client.get(
            f"https://redis.ayga.tech/kv/{result_key}",
            headers={"Authorization": f"Bearer {client._token}"}
        )
        
        print(f'  Status: {response.status_code}')
        
        if response.status_code == 200:
            print(f'  Raw response: {response.text[:500]}')
            try:
                result_json = response.json()
                print(f'  JSON keys: {list(result_json.keys())}')
                
                if "value" in result_json:
                    value_str = result_json["value"]
                    print(f'  Value type: {type(value_str)}')
                    print(f'  Value preview: {value_str[:500]}')
                    
                    # Try to parse A-Parser format
                    result_array = json.loads(value_str)
                    print(f'  Array length: {len(result_array)}')
                    print(f'  Array elements: {[type(x).__name__ for x in result_array]}')
                    
                    if len(result_array) >= 5:
                        task_id_ret, status, error_code, error_msg, data = result_array[:5]
                        print(f'  Task ID: {task_id_ret}')
                        print(f'  Status: {status}')
                        print(f'  Error code: {error_code}')
                        print(f'  Error msg: {error_msg}')
                        print(f'  Data type: {type(data).__name__}')
                        
                        if status == 'success':
                            print(f'✓ SUCCESS! Data: {json.dumps(data, indent=2)[:1000]}')
                            break
                        else:
                            print(f'  Still processing...')
                            
            except Exception as e:
                print(f'  Parse error: {e}')
                import traceback
                traceback.print_exc()
        elif response.status_code == 404:
            print(f'  Result not ready yet')
        else:
            print(f'  Error response: {response.text[:200]}')
        
        await asyncio.sleep(5)
    
    await client.close()


if __name__ == '__main__':
    asyncio.run(test())
