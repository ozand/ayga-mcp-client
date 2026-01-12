# v1.3.0 - Content, Social, Analytics & Visual Parsers

**39 parsers total** (was 29) - Added 10 new parsers across 4 categories.

## New Categories & Parsers

### Content Extraction (2 parsers)
- `article_extractor` - Extract articles with Mozilla Readability algorithm
- `text_extractor` - Parse text blocks with HTML cleaning (2000 queries/min)

### Social Media Expansion (6 parsers)
- `instagram_profile` - Profile data, posts, followers (requires auth cookie)
- `instagram_post` - Post with likes, comments, caption (up to 1200 comments)
- `instagram_tag` - Posts by hashtag (requires auth cookie)
- `instagram_geo` - Posts by location with coordinates
- `instagram_search` - Search profiles, hashtags, locations
- `tiktok_profile` - TikTok profile data, videos, followers

### Analytics (1 parser)
- `google_trends` - Keyword trends, interest data, regional analysis

### Visual Content (1 parser)
- `pinterest_search` - Pinterest images, titles, descriptions (4000+ queries/min)

## Statistics
- **Total parsers:** 29 → 39 (+34% increase)
- **Categories:** 6 → 9 (added Content, Analytics, Visual)
- **All tests passing:** 6/6 ✅

## Installation

```bash
pip install --upgrade ayga-mcp-client
```

## Usage Examples

```bash
# Instagram
@ayga parse_instagram_profile query="username" timeout=120
@ayga parse_instagram_tag query="travel" timeout=120

# TikTok
@ayga parse_tiktok_profile query="@username"

# Content extraction
@ayga parse_article_extractor query="https://example.com/article"

# Analytics
@ayga get_google_trends query="artificial intelligence"

# Visual content
@ayga search_pinterest_search query="modern interior design"
```

## Full Documentation
- GitHub: https://github.com/ozand/ayga-mcp-client
- PyPI: https://pypi.org/project/ayga-mcp-client/1.3.0/
