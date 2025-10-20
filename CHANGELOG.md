# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-10-20

### Changed
- **BREAKING**: `get_connection_stats` now raises `NotImplementedError` (endpoint not available in Fabric v4 API)
- **BREAKING**: `create_fabric_router` now raises `NotImplementedError` (write operations not available in Fabric v4 API)
- **BREAKING**: `update_fabric_router` now raises `NotImplementedError` (write operations not available in Fabric v4 API)
- **BREAKING**: `delete_fabric_router` now raises `NotImplementedError` (write operations not available in Fabric v4 API)
- `get_fabric_router` now uses search endpoint instead of direct GET (Fabric v4 compliance)
- Improved error messages for unsupported operations with alternative suggestions

### Added
- Clear `NotImplementedError` messages explaining why features are unavailable
- Suggestions for alternative approaches in error messages
- Better Fabric v4 API compliance
- Enhanced documentation for deprecated features
- New documentation files: API_LIMITATIONS.md, DEPRECATION_NOTICE.md
- Migration guide updates for v2.1 to v2.2

### Improved
- Router retrieval now properly uses `/fabric/v4/routers/search` endpoint
- Error handling provides actionable guidance
- Documentation clearly explains API limitations
- Migration guide for affected users

### Removed
- Connection statistics endpoint support (was non-functional)
- Cloud Router create operation support (was non-functional)
- Cloud Router update operation support (was non-functional)
- Cloud Router delete operation support (was non-functional)

### Fixed
- Router GET method now works correctly with search endpoint
- All API calls now align with Fabric v4 specifications
- Error messages now accurately reflect API capabilities

### Deprecated
The following features are deprecated due to Fabric v4 API limitations:

#### Connection Statistics (`get_connection_stats`)
- **Reason**: `/fabric/v4/connections/{uuid}/stats` endpoint does not exist
- **Alternative**: Use `get_fabric_connection()` for connection state and metadata
- **For Metrics**: Use Equinix Fabric Portal at https://fabric.equinix.com

#### Cloud Router Management
All write operations for Cloud Routers:
- **Reason**: Fabric v4 API does not expose write endpoints
- **Alternative Options**:
  1. Use Equinix Fabric Portal for GUI-based management
  2. Use Terraform with `equinix_fabric_cloud_router` resource
  3. Wait for potential Fabric v5 or v4 API updates
- **Note**: Read operations (list and get) continue to work via search endpoint

### Migration Notes

#### If You Use Connection Statistics
```python
# Old (v2.1) - No longer works
stats = get_connection_stats(
    connection_id="abc-123",
    from_ts="2025-01-01",
    to_ts="2025-01-31"
)

# New (v2.2) - Get connection metadata
connection = get_fabric_connection("abc-123")
print(f"State: {connection['state']}")
print(f"Bandwidth: {connection['bandwidth']} Mbps")

# For bandwidth graphs: Visit https://fabric.equinix.com
```

#### If You Manage Cloud Routers
**Option 1: Use Terraform (recommended for IaC)**
```hcl
resource "equinix_fabric_cloud_router" "example" {
  name         = "FCR-SG-PROD"
  type         = "XF_ROUTER"
  metro_code   = "SG"
  package_code = "PRO"
  
  project {
    project_id = var.project_id
  }
}
```

**Option 2**: Use Fabric Portal at https://fabric.equinix.com
- Navigate to Network → Cloud Routers
- Use GUI to create/update/delete routers

#### Read Operations Still Work
```python
# ✅ These continue to work
routers = list_fabric_routers()
router = get_fabric_router(router_uuid)
```

### Breaking Changes Summary

| Feature | v2.1 | v2.2 | Alternative |
|---------|------|------|-------------|
| get_connection_stats | ✅ | ❌ | Fabric Portal, get_fabric_connection() |
| create_fabric_router | ✅ | ❌ | Fabric Portal, Terraform |
| update_fabric_router | ✅ | ❌ | Fabric Portal, Terraform |
| delete_fabric_router | ✅ | ❌ | Fabric Portal, Terraform |
| get_fabric_router | ✅ | ✅ (via search) | - |
| list_fabric_routers | ✅ | ✅ (via search) | - |
| All other features | ✅ | ✅ | - |

### Documentation Updates

New documentation added:
- `API_LIMITATIONS.md` - Explains Fabric v4 API constraints
- `DEPRECATION_NOTICE.md` - Details on deprecated features
- `examples/monitoring_without_stats.md` - Alternative monitoring approaches
- `examples/TERRAFORM_GUIDE.md` - Cloud Router management with Terraform
- Updated `MIGRATION.md` - Comprehensive migration guide
- Updated `FAQ.md` - v2.2 specific questions
- Updated `ARCHITECTURE.md` - API version limitations section

### What Still Works

All core functionality remains intact:
- ✅ Port management (list, get)
- ✅ Connection management (full CRUD, search, validate)
- ✅ Cloud Router viewing (list, get via search)
- ✅ Service profiles (list, get)
- ✅ Service tokens (full CRUD)
- ✅ Metro locations (list)
- ✅ OAuth2 authentication
- ✅ Token caching
- ✅ All Python 3.10+ features

---

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

---

## Migration Guide

### From v2.1 to v2.2

**Impact**: Low for most users

#### What Changed
1. Connection statistics API removed (not available in Fabric v4)
2. Cloud Router write operations removed (not available in Fabric v4)
3. Cloud Router read operations now use search endpoint

#### Action Required

**If you use connection statistics:**
- Replace with `get_fabric_connection()` for state/metadata
- Use Fabric Portal for bandwidth graphs

**If you manage Cloud Routers:**
- Migrate to Fabric Portal (GUI)
- Or use Terraform for Infrastructure as Code

**If you only read Cloud Routers:**
- No changes needed - continues to work via search

#### Testing
```python
# Test that deprecated features raise clear errors
try:
    get_connection_stats("test-id")
except NotImplementedError as e:
    print(f"Expected: {e}")  # Should provide alternatives
```

For detailed migration instructions, see [MIGRATION.md](MIGRATION.md).

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

- All MCP tools work identically (with v2.2 deprecations noted above)
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

---

## Version History

- **2.2.0** - Fabric v4 API compliance (Current)
- **2.1.0** - Python rewrite with OAuth2
- **1.0.0** - Initial TypeScript release

## Security

### v2.2.0 Security Notes
- No security changes from v2.1.0
- Deprecated features were already non-functional
- OAuth2 authentication continues unchanged

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
**Migration Support**: See [MIGRATION.md](MIGRATION.md) or open an issue