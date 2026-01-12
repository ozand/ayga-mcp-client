# Release v1.0.2 - Maintenance Release

## Summary
Maintenance release addressing package consistency issues identified in external audit.

## Fixed
- ✅ **Version Synchronization**: Fixed `__version__` in `__init__.py` (was 1.0.0, now matches package version 1.0.2)
- ✅ **Package Cleanup**: Removed unused `tools/` directory from package structure

## Technical Details
- All functionality from v1.0.1 preserved
- No breaking changes
- Package size reduced by removing empty directory
- Version consistency across all package files

## Upgrade Instructions
```bash
pip install --upgrade ayga-mcp-client
```

## Links
- **PyPI**: https://pypi.org/project/ayga-mcp-client/1.0.2/
- **GitHub**: https://github.com/ozand/ayga-mcp-client
- **Documentation**: README.md

---
**Full Changelog**: https://github.com/ozand/ayga-mcp-client/compare/v1.0.1...v1.0.2
