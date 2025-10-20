# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-10-20

### Fixed
- **CRITICAL**: Corrected documentation to reflect actual Fabric v4 API capabilities
- Marked Cloud Router create/update/delete operations as unsupported (read-only in v4)
- Deprecated `get_connection_stats` tool (endpoint not available in Fabric v4 API)
- Updated tool count from 21 to 22 (accurate count)
- Added `get_service_token` tool to Service Tokens section

### Added
- Clear "Known API Limitations" section in README
- NotImplementedError exceptions for unsupported operations with helpful messages
- API Limitation Errors troubleshooting section
- Workarounds for deprecated/unsupported features
- Version 2.2 updates section highlighting changes

### Changed
- Cloud Router operations now use search endpoints (GET only)
- Connection statistics replaced with connection metadata retrieval
- Updated usage examples to reflect working features only
- Enhanced error messages for better user experience
- Improved troubleshooting documentation

### Documentation
- README updated with accurate feature descriptions
- Strikethrough formatting for deprecated/unsupported features
- Warning callouts for API limitations
- Clear separation of working vs non-working features
- Updated version and last modified date

## [2.1.0] - 2025-10-18

### Changed
- **BREAKING**: Migrated from TypeScript/Node.js to Python 3.10+
- **BREAKING**: Authentication changed from Bearer token to OAuth2 Client Credentials
  - Old: `EQUINIX_API_TOKEN` environment variable
  - New: `EQUINIX_CLIENT_ID` + `EQUINIX_CLIENT_SECRET` environment variables
- Complete rewrite using Python MCP SDK
- Improved async/await implementation throughout

### Added
- OAuth2 authentication with automatic token refresh
- Token caching for improved performance (60-second safety margin)
- Python packaging with pyproject.toml
- Support for Python 3.10, 3.11, and 3.12
- Type hints throughout the codebase
- Better error handling and reporting

### Improved
- More secure authentication method (OAuth2 vs static tokens)
- Better performance with token caching
- Cleaner code structure
- Native Python async/await patterns

### Removed
- TypeScript/Node.js implementation
- npm package configuration
- Node.js dependencies

## [1.0.0] - 2025-10-18 (TypeScript version)

### Added
- Initial release of Equinix Fabric MCP Server (TypeScript)
- Port management tools (list, get)
- Connection management tools (list, get, create, update, delete, stats, search, validate)
- Cloud Router management tools (list, get, create, update, delete)
- Service Profile tools (list, get)
- Service Token tools (list, get, create, delete)
- Metro location listing
- Comprehensive documentation (README, USAGE, CONTRIBUTING)
- TypeScript implementation with MCP SDK
- GitHub Actions CI workflow
- MIT License

### Features (v1.0)

#### Port Management
- List all Fabric ports with pagination
- Get detailed port information by UUID

#### Connection Management
- List connections with filtering and pagination
- Get detailed connection information
- Create virtual connections (EVPL, EPL, IPWAN, EPLAN, EVPLAN)
- Update connection properties (bandwidth, name, description)
- Delete connections
- Get connection statistics and bandwidth usage
- Search connections by name and state
- Validate connection configurations

#### Cloud Router Management
- List all Cloud Routers
- Get router details and BGP configuration
- Create routers with package selection (STANDARD, PRO, ADVANCED)
- Update router configurations
- Delete routers

#### Service Profiles & Tokens
- List available service profiles (AWS, Azure, GCP, Oracle, IBM, etc.)
- Get service profile details
- Create service tokens for partner access
- List and manage service tokens
- Delete service tokens

#### Infrastructure
- List all Equinix metro locations
- API error handling and reporting
- Environment-based configuration
- Secure token management

## [Unreleased]

### Planned
- Automated testing suite
- Enhanced usage statistics and metrics
- Performance monitoring tools
- Batch operations support

### Under Consideration
- Connection templates
- Cost optimization recommendations
- Integration with other MCP servers
- Connection health monitoring
- Performance analytics dashboard
- Webhook support for real-time updates

---

## Migration Guide

### From v2.1 to v2.2

#### No Breaking Changes
Version 2.2 is a **documentation update only** - no code changes required.

#### What Changed
- Documentation now accurately reflects Fabric v4 API limitations
- Cloud Router CRUD operations marked as unsupported (API limitation)
- Connection statistics marked as deprecated (API limitation)
- Better error messages when attempting unsupported operations

#### Action Required
- **None** - Your existing configuration continues to work
- Review Known API Limitations section in README
- Update any scripts that use unsupported features

#### Deprecated Features
- ❌ `get_connection_stats` - Use `get_fabric_connection` instead
- ❌ `create_fabric_router` - Use Equinix Portal instead
- ❌ `update_fabric_router` - Use Equinix Portal instead
- ❌ `delete_fabric_router` - Use Equinix Portal instead

### From v1.0 (TypeScript) to v2.1+ (Python)

#### Prerequisites
1. **Python 3.10+** instead of Node.js 18+
2. **OAuth2 credentials** instead of API token

#### Installation Changes

**Old (v1.0)**:
```bash
npm install -g equinix-fabric-mcp
```

**New (v2.1+)**:
```bash
pip install equinix-fabric-mcp
```

#### Configuration Changes

**Old Claude Desktop config (v1.0)**:
```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

**New Claude Desktop config (v2.1+)**:
```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "EQUINIX_CLIENT_ID": "your-client-id",
        "EQUINIX_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

#### Getting OAuth2 Credentials

1. Log in to Equinix Fabric Portal
2. Go to User Settings → API
3. Create OAuth2 Application
4. Save Client ID and Client Secret

#### What Stays the Same

- Core MCP tools work identically
- Tool names and parameters unchanged (working features)
- API endpoints remain the same
- Functionality is preserved (for supported features)
- Documentation structure maintained

#### Benefits of Migration

- ✅ More secure OAuth2 authentication
- ✅ Automatic token refresh
- ✅ Better performance with caching
- ✅ Native Python async/await
- ✅ Improved error handling
- ✅ Type safety with Python type hints
- ✅ Accurate documentation of API limitations

## Version History

- **2.2.0** - Documentation accuracy update (Current)
- **2.1.0** - Python rewrite with OAuth2
- **1.0.0** - Initial TypeScript release

## Breaking Changes Summary

### v2.2.0
- **Documentation only** - no code breaking changes
- Clarified unsupported features (were never working in v2.1)

### v2.1.0
- Language changed from TypeScript to Python
- Authentication method changed from API token to OAuth2
- Installation method changed from npm to pip
- Configuration format updated for Python

## Known Issues & Limitations

### Fabric v4 API Limitations (v2.2+)
These are **API limitations**, not bugs in the MCP server:

1. **Connection Statistics**
   - Endpoint `/fabric/v4/connections/{id}/stats` not available
   - **Workaround**: Use `get_fabric_connection` for metadata

2. **Cloud Router CRUD**
   - POST/PATCH/DELETE operations not available in v4 API
   - **Workaround**: Manage through Equinix Portal
   - **Still works**: List and Get router information

3. **Route Filters**
   - Not yet exposed in Fabric v4 API
   - Planned for future API updates

### Reporting Issues

If you encounter an issue:
1. Check if it's a known API limitation (above)
2. Verify your OAuth2 credentials are valid
3. Check Claude Desktop logs for details
4. Open a GitHub issue with reproduction steps

## Security

### v2.2.0 Security Notes
- No security changes (documentation update only)
- All v2.1.0 security features remain

### v2.1.0 Security Enhancements
- OAuth2 Client Credentials flow (more secure than static tokens)
- Automatic token refresh (reduces exposure window)
- Token caching (minimizes API calls)
- Environment variable isolation
- No token persistence

### Security Recommendations
- Rotate OAuth2 credentials every 90 days
- Use separate credentials per environment
- Enable API access logging
- Monitor for unauthorized access
- Follow principle of least privilege

For security issues, please create a private security advisory on GitHub.

---

**Changelog Version**: 2.2.0  
**Last Updated**: October 20, 2025  
**Migration Support**: See migration guide above or open an issue
