# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### Planned for v2.2
- Automated testing suite
- Route filter management
- Network operations support
- Enhanced usage statistics
- Performance monitoring tools
- Batch operations support

### Under Consideration
- GraphQL support
- Connection templates
- Cost optimization recommendations
- Automated failover management
- Integration with other MCP servers
- Connection health monitoring
- Performance analytics dashboard
- Webhook support for real-time updates

---

## Migration Guide

### From v1.0 (TypeScript) to v2.1 (Python)

#### Prerequisites
1. **Python 3.10+** instead of Node.js 18+
2. **OAuth2 credentials** instead of API token

#### Installation Changes

**Old (v1.0)**:
```bash
npm install -g equinix-fabric-mcp
```

**New (v2.1)**:
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

**New Claude Desktop config (v2.1)**:
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

- All 21 MCP tools work identically
- Tool names and parameters unchanged
- API endpoints remain the same
- Functionality is preserved
- Documentation structure maintained

#### Benefits of Migration

- ✅ More secure OAuth2 authentication
- ✅ Automatic token refresh
- ✅ Better performance with caching
- ✅ Native Python async/await
- ✅ Improved error handling
- ✅ Type safety with Python type hints

## Version History

- **2.1.0** - Python rewrite with OAuth2 (Current)
- **1.0.0** - Initial TypeScript release

## Breaking Changes Summary

### v2.1.0
- Language changed from TypeScript to Python
- Authentication method changed from API token to OAuth2
- Installation method changed from npm to pip
- Configuration format updated for Python

## Security

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

**Changelog Version**: 2.1.0  
**Last Updated**: October 18, 2025  
**Migration Support**: See migration guide above or open an issue
