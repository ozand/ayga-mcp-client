# Release Notes v1.4.1 - Version Synchronization & PyPI Update

## 🎯 Overview

Synchronization release to align PyPI package metadata with actual parser count and GitHub releases. This ensures accurate documentation across all distribution channels.

## ✨ What's Fixed

### PyPI Metadata Update
- **Corrected parser count**: Now accurately shows 40 parsers (was incorrectly showing 39 in PyPI metadata)
- **Enhanced description**: Added all 9 parser categories for better discoverability
- **Version alignment**: PyPI, GitHub, and local code now all show v1.4.1

### Documentation Improvements
- Updated project description to include all parser categories
- Synchronized README with package metadata
- Improved PyPI search results with complete category list

## 📊 Parser Breakdown (40 Total)

### Category Distribution
- **FreeAI Parsers** (6): Perplexity, ChatGPT, GoogleAI, Kimi, DeepAI, Copilot
- **YouTube Parsers** (6): Video metadata, search, suggestions, channel info, comments
- **Social Media** (10): Instagram (6), TikTok (1), Telegram, Reddit (3)
- **Translation** (4): Google, DeepL, Bing, Yandex
- **Search Engines** (8): Google, Yandex, Bing, DuckDuckGo, Baidu, Yahoo, Rambler, You.com
- **Content** (3): Article extractor, Text extractor, Link extractor ⭐ NEW
- **Analytics** (1): Google Trends
- **Visual** (1): Pinterest search
- **Net Tools** (1): HTTP fetcher

## 🔧 Technical Changes

### Package Metadata
```toml
version = "1.4.1"
description = "MCP server for Redis API with 40 AI parsers across 9 categories"
```

### PyPI Synchronization
- Package rebuilt and verified with twine
- Full distribution uploaded (wheel + sdist)
- Metadata cached and indexed by PyPI

## 📚 Documentation Status

### Updated Documentation
- ✅ README.md - Accurate parser count and categories
- ✅ CHANGELOG.md - New v1.4.1 entry with fixes
- ✅ pyproject.toml - Correct version and description
- ✅ PyPI package page - Updated metadata

### User-Facing Documentation
- Quick Start guide: Works with all 40 parsers
- Example usage: Links to Link Extractor and other content parsers
- Installation instructions: Updated for v1.4.1

## 🚀 Installation

### Install Latest Version
```bash
pip install --upgrade ayga-mcp-client
```

### Verify Installation
```bash
python -c "import ayga_mcp_client; print('✅ ayga-mcp-client installed')"
```

### Check Available Parsers
```bash
python -m ayga_mcp_client --help
```

## 🔗 Related Releases

- **redis_wrapper v2.1.0**: Added Link Extractor parser to backend
- **ayga-mcp-client v1.4.0**: Initial Link Extractor support
- **ayga-mcp-client v1.4.1**: This release - PyPI synchronization

## ⚠️ Breaking Changes

None - Fully backward compatible with v1.4.0 and earlier versions.

## 🐛 Bug Fixes

- Fixed PyPI package showing 39 parsers instead of 40
- Corrected version discrepancy between PyPI and GitHub
- Synchronized metadata across all distribution channels

## 📦 Package Contents

### Distribution Files
- `ayga_mcp_client-1.4.1-py3-none-any.whl` - Wheel package for pip
- `ayga_mcp_client-1.4.1.tar.gz` - Source distribution (sdist)

### Build Information
- Python 3.11+
- All dependencies included in wheel
- MCP SDK v1.0.0+

## 🎓 Usage Examples

### All 40 Parsers Available via MCP Tools

```bash
# FreeAI parsers
@ayga search_perplexity query="AI trends"

# Content parsers (including new link extractor)
@ayga parse_link_extractor query="https://example.com" preset="deep_crawl"
@ayga parse_article_extractor query="https://news.example.com"

# YouTube, Social Media, Search, etc.
# All 40 parsers work seamlessly
```

## 🔮 What's Next

- Continued parser additions and improvements
- Enhanced documentation and examples
- Performance optimizations based on usage patterns
- Integration improvements for Claude Desktop and VS Code

---

**Installation**: `pip install ayga-mcp-client==1.4.1`  
**GitHub**: https://github.com/ozand/ayga-mcp-client  
**PyPI**: https://pypi.org/project/ayga-mcp-client/  
**Documentation**: See README.md and DEVELOPMENT.md  
**Support**: support@ayga.tech
