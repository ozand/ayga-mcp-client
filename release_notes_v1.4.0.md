# Release Notes v1.4.0 - Domain Scraping Enhancement

**Release Date**: 2026-01-14  
**Type**: Minor Release (Feature Addition)

## 🎯 Overview

Version 1.4.0 adds Link Extractor parser for domain scraping workflows, enabling AI agents to orchestrate complex content collection tasks across multiple pages and domains.

## ✨ New Features

### Link Extractor Parser

**Tool**: `extract_link_extractor`

Extract all links from HTML pages with advanced filtering and multi-level crawling:

- ✅ **Multi-level crawling**: Depth 1-5 for deep domain exploration
- ✅ **Link filtering**: Separate internal and external links
- ✅ **Automatic deduplication**: No duplicate URLs in results
- ✅ **CloudFlare bypass**: Works with protected sites
- ✅ **3 Presets**:
  - `default` - Single page, internal links only
  - `deep_crawl` - Multi-level crawl up to 3 levels
  - `all_links` - Extract both internal and external links

**Performance**:
- Rate limit: 500 queries/min
- Response time: 3-10 seconds per page
- Default timeout: 120 seconds

## 📊 Statistics

- **Total parsers**: 40 (was 39)
- **Content category**: 3 parsers (Article, Text, Link Extractors)
- **New tools**: 1

## 🚀 Usage Examples

### Basic Link Extraction

```
@ayga extract_link_extractor 
query="https://maze.co/resources" 
preset="default"
```

**Returns**:
```json
{
  "links": ["https://maze.co/resources/article-1", ...],
  "total_count": 50,
  "internal_count": 50,
  "external_count": 0
}
```

### Deep Crawl

```
@ayga extract_link_extractor 
query="https://example.com" 
preset="deep_crawl" 
timeout=180
```

### Agent Orchestration Workflow

**Scenario**: Collect all articles from a domain

```
Step 1: Extract links
@ayga extract_link_extractor 
query="https://maze.co/resources" 
preset="deep_crawl"

Step 2: For each link, extract article
@ayga parse_article_extractor 
query="{link_url}"

Step 3: Agent merges results into single file
→ "Saved 50 articles to maze_articles.md"
```

## 🏗️ Architecture

### Agent Orchestration Pattern

Link Extractor is designed for **Agent Orchestration** rather than built-in flows:

**Why?**
- ✅ **Flexibility**: Agent adapts to intermediate results
- ✅ **Visibility**: Each step visible in chat
- ✅ **Retry Logic**: Agent can retry failed steps
- ✅ **Thin Client**: Business logic stays in agent, not client
- ✅ **Extensibility**: Easy to add new parsers without flow changes

## 🔧 Technical Changes

### Modified Files

```
src/ayga_mcp_client/server.py
- Added link_extractor to PARSERS list
- Added to medium timeout category (120s)
- Added preset enum validation in input schema

README.md
- Updated parser count: 39 → 40
- Added link_extractor to Content category

CHANGELOG.md
- Added v1.4.0 entry with all changes

pyproject.toml
- Version bump: 1.3.1 → 1.4.0
- Updated description with parser count
```

## 📦 Installation

### Update Existing Installation

```bash
pip install --upgrade ayga-mcp-client
```

### Fresh Installation

```bash
pip install ayga-mcp-client==1.4.0
```

### Verify Version

```bash
python -c "import ayga_mcp_client; print(ayga_mcp_client.__version__)"
# Output: 1.4.0
```

## 🧪 Testing

### Test Link Extractor

```bash
# Set API key
export REDIS_API_KEY="your_api_key"

# Run MCP client
python -m ayga_mcp_client

# Test via Claude/Cursor
@ayga extract_link_extractor query="https://example.com" preset="default"
```

## 📚 Documentation Updates

- ✅ README.md updated with v1.4.0 features
- ✅ CHANGELOG.md with full change history
- ✅ Examples for domain scraping workflows
- ✅ Agent Orchestration pattern documentation

## 🔄 Migration Guide

### From v1.3.1 to v1.4.0

**Breaking Changes**: None ✅

**New Features**:
- Link Extractor available immediately after update
- No configuration changes required
- Backward compatible with v1.3.x

**Recommended Actions**:
1. Update package: `pip install --upgrade ayga-mcp-client`
2. Restart Claude Desktop/VS Code
3. Test link_extractor: `@ayga extract_link_extractor query="https://example.com"`

## 🎯 Use Cases

### 1. Domain Content Collection

Collect all articles from a domain for analysis or archiving.

### 2. SEO Analysis

Extract all internal/external links to analyze site structure.

### 3. Competitor Research

Map competitor website structure and content organization.

### 4. Documentation Scraping

Collect all documentation pages from a product site.

### 5. News Aggregation

Extract article links from news sites for processing.

## 🐛 Known Issues

None reported for v1.4.0.

## 🔮 Future Roadmap

### v1.5.0 (Planned)
- Enhanced link filtering with regex patterns
- Link metadata extraction (title, description)
- Sitemap parsing support
- Broken link detection

### v1.6.0 (Planned)
- Custom crawl rules
- Rate limiting per domain
- Parallel link extraction

## 📞 Support

- **API Access**: https://redis.ayga.tech
- **Documentation**: [README.md](README.md)
- **Examples**: [EXAMPLES.md](EXAMPLES.md)
- **Technical Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)
- **Issues**: GitHub Issues
- **Email**: support@ayga.tech

## 🙏 Credits

- **Backend**: redis_wrapper v2.0 with Parser Registry architecture
- **A-Parser Integration**: HTML::LinkExtractor parser
- **MCP Protocol**: Anthropic Model Context Protocol

---

**Full Changelog**: https://github.com/ozand/ayga-mcp-client/blob/main/CHANGELOG.md
