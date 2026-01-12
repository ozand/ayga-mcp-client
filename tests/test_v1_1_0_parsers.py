"""Test ayga-mcp-client v1.3.0 - verify all 39 parsers are available."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ayga_mcp_client.server import PARSERS, get_parser_input_schema


def test_parser_count():
    """Verify we have exactly 39 parsers."""
    assert len(PARSERS) == 39, f"Expected 39 parsers, got {len(PARSERS)}"
    print(f"✓ Parser count: {len(PARSERS)}")


def test_parser_categories():
    """Verify parsers are in correct categories."""
    categories = {
        "FreeAI": ["perplexity", "googleai", "chatgpt", "kimi", "deepai", "copilot"],
        "YouTube": ["youtube_video", "youtube_search", "youtube_suggest", 
                   "youtube_channel_videos", "youtube_channel_about", "youtube_comments"],
        "Social": ["telegram_group", "reddit_posts", "reddit_post_info", "reddit_comments",
                  "instagram_profile", "instagram_post", "instagram_tag", "instagram_geo", 
                  "instagram_search", "tiktok_profile"],
        "Translation": ["google_translate", "deepl_translate", "bing_translate", "yandex_translate"],
        "SE": ["google_search", "yandex_search", "bing_search", "duckduckgo_search",
               "baidu_search", "yahoo_search", "rambler_search", "you_search"],
        "Content": ["article_extractor", "text_extractor"],
        "Analytics": ["google_trends"],
        "Visual": ["pinterest_search"],
        "Net": ["http"]
    }
    
    parser_ids = [p["id"] for p in PARSERS]
    
    for category, expected_ids in categories.items():
        for pid in expected_ids:
            assert pid in parser_ids, f"Missing {category} parser: {pid}"
        print(f"✓ {category} parsers ({len(expected_ids)}): all present")


def test_parser_structure():
    """Verify each parser has required fields."""
    required_fields = ["id", "name", "description", "prefix"]
    
    for parser in PARSERS:
        for field in required_fields:
            assert field in parser, f"Parser {parser.get('id', 'unknown')} missing field: {field}"
    
    print(f"✓ All parsers have required fields: {', '.join(required_fields)}")


def test_tool_prefixes():
    """Verify tool prefixes are correct."""
    prefix_map = {
        "search_": ["perplexity", "googleai", "chatgpt", "kimi", "deepai", "copilot",
                   "youtube_search", "reddit_posts", "reddit_comments",
                   "google_search", "yandex_search", "bing_search", "duckduckgo_search",
                   "baidu_search", "yahoo_search", "rambler_search", "you_search",
                   "instagram_search", "pinterest_search"],
        "parse_": ["youtube_video", "youtube_comments", 
                  "instagram_profile", "instagram_post", "instagram_tag", "instagram_geo",
                  "tiktok_profile", "article_extractor", "text_extractor"],
        "get_": ["youtube_suggest", "youtube_channel_videos", "youtube_channel_about", 
                "reddit_post_info", "google_trends"],
        "translate_": ["google_translate", "deepl_translate", "bing_translate", "yandex_translate"],
        "scrape_": ["telegram_group"],
        "fetch_": ["http"]
    }
    
    for parser in PARSERS:
        pid = parser["id"]
        prefix = parser["prefix"]
        
        # Find expected prefix
        expected_prefix = None
        for exp_prefix, parser_list in prefix_map.items():
            if pid in parser_list:
                expected_prefix = exp_prefix
                break
        
        assert expected_prefix is not None, f"Parser {pid} not in prefix map"
        assert prefix == expected_prefix, f"Parser {pid} has prefix '{prefix}', expected '{expected_prefix}'"
    
    print(f"✓ All tool prefixes are correct")


def test_input_schemas():
    """Verify input schemas are generated correctly."""
    # Test base schema
    perplexity = next(p for p in PARSERS if p["id"] == "perplexity")
    schema = get_parser_input_schema(perplexity)
    assert "query" in schema["properties"], "Base schema missing 'query'"
    assert "timeout" in schema["properties"], "Base schema missing 'timeout'"
    assert "preset" in schema["properties"], "Base schema missing 'preset'"
    print("✓ Base schema (FreeAI): query, timeout, preset")
    
    # Test YouTube extended schema
    youtube_video = next(p for p in PARSERS if p["id"] == "youtube_video")
    schema = get_parser_input_schema(youtube_video)
    assert "interface_language" in schema["properties"], "YouTube schema missing 'interface_language'"
    assert "subtitles_language" in schema["properties"], "YouTube schema missing 'subtitles_language'"
    assert "comments_pages" in schema["properties"], "YouTube schema missing 'comments_pages'"
    print("✓ YouTube schema: base + interface_language, subtitles_language, comments_pages")
    
    # Test Translation schema
    google_translate = next(p for p in PARSERS if p["id"] == "google_translate")
    schema = get_parser_input_schema(google_translate)
    assert "from_language" in schema["properties"], "Translation schema missing 'from_language'"
    assert "to_language" in schema["properties"], "Translation schema missing 'to_language'"
    print("✓ Translation schema: base + from_language, to_language")
    
    # Test Social schema
    reddit_posts = next(p for p in PARSERS if p["id"] == "reddit_posts")
    schema = get_parser_input_schema(reddit_posts)
    assert "pages_count" in schema["properties"], "Social schema missing 'pages_count'"
    assert "sort" in schema["properties"], "Social schema missing 'sort'"
    print("✓ Social schema: base + pages_count, sort")


def test_a_parser_mapping():
    """Verify A-Parser name mappings exist in client.py."""
    from ayga_mcp_client.api.client import RedisAPIClient
    
    # Read the parser_map from client.py source
    import inspect
    source = inspect.getsource(RedisAPIClient.submit_parser_task)
    
    # Check critical mappings (including new v1.3.0 parsers)
    critical_mappings = [
        ("perplexity", "FreeAI::Perplexity"),
        ("youtube_video", "SE::YouTube::Video"),
        ("telegram_group", "Telegram::GroupScraper"),
        ("google_translate", "SE::Google::Translate"),
        ("instagram_profile", "Social::Instagram::Profile"),
        ("instagram_post", "Social::Instagram::Post"),
        ("tiktok_profile", "Social::TikTok::Profile"),
        ("article_extractor", "HTML::ArticleExtractor"),
        ("text_extractor", "HTML::TextExtractor"),
        ("google_trends", "SE::Google::Trends"),
        ("pinterest_search", "SE::Pinterest"),
        ("http", "Net::HTTP"),
    ]
    
    for parser_id, aparser_name in critical_mappings:
        assert f'"{parser_id}": "{aparser_name}"' in source, \
            f"Missing mapping: {parser_id} → {aparser_name}"
    
    print(f"✓ A-Parser mappings present for all critical parsers")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_parser_count,
        test_parser_categories,
        test_parser_structure,
        test_tool_prefixes,
        test_input_schemas,
        test_a_parser_mapping,
    ]
    
    print("\n=== Testing ayga-mcp-client v1.2.0 ===\n")
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error: {e}")
            failed += 1
    
    print(f"\n=== Results ===")
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ All tests passed! ayga-mcp-client v1.2.0 is ready.")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
