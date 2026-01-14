#!/usr/bin/env python3
"""Test link_extractor parser."""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ayga_mcp_client.api.client import RedisAPIClient


async def test_link_extractor():
    """Test link_extractor parser."""
    
    # Get API key from environment
    api_key = os.getenv("REDIS_API_KEY")
    if not api_key:
        print("❌ REDIS_API_KEY environment variable not set")
        print("   Set it with: export REDIS_API_KEY='your_key_here'")
        return False
    
    print("\n" + "="*60)
    print("Testing Link Extractor Parser")
    print("="*60)
    
    try:
        client = RedisAPIClient(api_key=api_key)
        
        # Test 1: Basic link extraction
        print("\n📋 Test 1: Basic link extraction (default preset)")
        print("   URL: https://example.com")
        
        result = await client.submit_parser_task(
            "link_extractor",
            query="https://example.com",
            options={"preset": "default"}
        )
        
        task_id = result.get("task_id")
        print(f"   ✅ Task submitted: {task_id}")
        
        # Wait for result
        print("   ⏳ Waiting for result (timeout: 120s)...")
        result = await client.wait_for_result(task_id, timeout=120)
        
        if "data" in result:
            data = result["data"]
            if isinstance(data, dict):
                links = data.get("links", [])
                total = data.get("total_count", 0)
                internal = data.get("internal_count", 0)
                external = data.get("external_count", 0)
                
                print(f"   ✅ Links extracted: {total}")
                print(f"   ✅ Internal: {internal}, External: {external}")
                
                if links:
                    print(f"   ✅ Sample links:")
                    for link in links[:3]:
                        print(f"      - {link}")
            else:
                print(f"   ℹ️  Raw data: {data}")
        else:
            print(f"   ⚠️  Result: {result}")
        
        print("\n✅ Test 1 completed")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_link_extractor_presets():
    """Test link_extractor with different presets."""
    
    api_key = os.getenv("REDIS_API_KEY")
    if not api_key:
        print("❌ REDIS_API_KEY not set")
        return False
    
    print("\n" + "="*60)
    print("Testing Link Extractor Presets")
    print("="*60)
    
    try:
        client = RedisAPIClient(api_key=api_key)
        
        presets = ["default", "deep_crawl", "all_links"]
        
        for preset in presets:
            print(f"\n📋 Testing preset: {preset}")
            
            result = await client.submit_parser_task(
                "link_extractor",
                query="https://example.com",
                options={"preset": preset, "timeout": 120}
            )
            
            task_id = result.get("task_id")
            print(f"   ✅ Task submitted with preset '{preset}': {task_id}")
        
        print("\n✅ All presets tested (tasks submitted)")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_parser_info():
    """Test getting parser info for link_extractor."""
    
    api_key = os.getenv("REDIS_API_KEY")
    if not api_key:
        print("❌ REDIS_API_KEY not set")
        return False
    
    print("\n" + "="*60)
    print("Testing Parser Info")
    print("="*60)
    
    try:
        client = RedisAPIClient(api_key=api_key)
        
        print("\n📋 Getting link_extractor info...")
        info = await client.get_parser_info("link_extractor")
        
        if "metadata" in info:
            metadata = info["metadata"]
            print(f"   ✅ Name: {metadata.get('name')}")
            print(f"   ✅ Description: {metadata.get('description')}")
            print(f"   ✅ Category: {info.get('category')}")
            print(f"   ✅ Icon: {metadata.get('icon')}")
        
        if "presets" in info:
            print(f"   ✅ Presets: {len(info['presets'])}")
            for preset_name, preset_data in info["presets"].items():
                print(f"      - {preset_name}: {preset_data.get('name', preset_name)}")
        
        if "parameters" in info:
            print(f"   ✅ Parameters: {len(info['parameters'])}")
        
        print("\n✅ Parser info retrieved")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests() -> int:
    """Run all tests."""
    print("\n" + "="*60)
    print("LINK EXTRACTOR TEST SUITE")
    print("="*60)
    
    tests = [
        ("Basic Link Extraction", test_link_extractor),
        ("Parser Presets", test_link_extractor_presets),
        ("Parser Info", test_parser_info),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = asyncio.run(test_func())
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
