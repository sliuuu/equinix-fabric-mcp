# Migration Guide: v1.0 (TypeScript) to v2.1 (Python)

This guide helps you migrate from the TypeScript/Node.js implementation (v1.0) to the Python implementation (v2.1).

## ⚠️ Breaking Changes

### 1. Programming Language
- **Old**: TypeScript/Node.js
- **New**: Python 3.10+

### 2. Authentication Method
- **Old**: Bearer token (API key)
  - Environment variable: `EQUINIX_API_TOKEN`
- **New**: OAuth2 Client Credentials
  - Environment variables: `EQUINIX_CLIENT_ID` + `EQUINIX_CLIENT_SECRET`

### 3. Installation Method
- **Old**: npm/npx
- **New**: pip

## 🛠️ Migration Steps

### Step 1: Uninstall Old Version

```bash
# Remove npm package
npm uninstall -g equinix-fabric-mcp

# Or if you had it locally
rm -rf /path/to/equinix-fabric-mcp
```

### Step 2: Install Python Version

**Verify Python version** (must be 3.10+):
```bash
python --version
```

**Install the new version**:
```bash
pip install equinix-fabric-mcp
```

### Step 3: Get OAuth2 Credentials

You need to **replace your API token** with OAuth2 credentials:

1. Log in to [Equinix Fabric Portal](https://fabric.equinix.com)
2. Navigate to **User Settings** → **API**
3. Click **Create OAuth2 Application**
4. Name it (e.g., "Claude MCP v2.1")
5. Copy both:
   - **Client ID**
   - **Client Secret**
6. Store them securely

### Step 4: Update Claude Desktop Configuration

**Old configuration (v1.0)**:
```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "your-old-token"
      }
    }
  }
}
```

**New configuration (v2.1)**:
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

**Or if using pip installation**:
```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "equinix-fabric-mcp",
      "env": {
        "EQUINIX_CLIENT_ID": "your-client-id",
        "EQUINIX_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

### Step 5: Restart Claude Desktop

Completely quit and reopen Claude Desktop.

### Step 6: Verify Migration

Test with a simple command:
```
List all my Fabric ports
```

If you see results, migration is complete!

## ✅ What Remains the Same

### Tool Names & Functionality
All 21 tools work identically:
- `list_fabric_ports`
- `get_fabric_port`
- `list_fabric_connections`
- `get_fabric_connection`
- `create_fabric_connection`
- `update_connection`
- `delete_connection`
- `get_connection_stats`
- `list_fabric_routers`
- `get_fabric_router`
- `create_fabric_router`
- `update_fabric_router`
- `delete_fabric_router`
- `search_connections`
- `list_metros`
- `list_service_profiles`
- `get_service_profile`
- `create_service_token`
- `list_service_tokens`
- `get_service_token`
- `delete_service_token`

### Tool Parameters
All parameters remain the same:
- Connection creation schemas unchanged
- Router creation parameters identical
- Service token formats preserved

### API Endpoints
All Equinix Fabric API v4 endpoints:
- `/fabric/v4/ports`
- `/fabric/v4/connections`
- `/fabric/v4/cloudRouters`
- `/fabric/v4/serviceProfiles`
- `/fabric/v4/serviceTokens`
- `/fabric/v4/metros`

### User Experience
No changes to how you interact with Claude:
- Same natural language commands
- Same response formats
- Same capabilities

## 🆕 What's Better in v2.1

### Security
- ✅ **OAuth2 authentication** (industry standard)
- ✅ **Automatic token refresh** (more reliable)
- ✅ **Shorter token lifetime** (reduced exposure)
- ✅ **Revocable credentials** (better control)

### Performance
- ✅ **Token caching** (fewer API calls)
- ✅ **Native async/await** (better concurrency)
- ✅ **Optimized for Python** (language advantages)

### Developer Experience
- ✅ **Type hints** (better IDE support)
- ✅ **Simpler codebase** (easier to contribute)
- ✅ **Python ecosystem** (more libraries)

## 🚨 Common Migration Issues

### Issue 1: Python Not Found

**Error**: `command not found: python`

**Solution**:
```bash
# Try python3
which python3

# Update config to use python3
"command": "python3"
```

### Issue 2: Wrong Python Version

**Error**: Module requires Python 3.10+

**Solution**:
```bash
# Check version
python --version

# Install Python 3.10+ from python.org
# Or use pyenv:
pyenv install 3.12
pyenv global 3.12
```

### Issue 3: OAuth2 Credentials Invalid

**Error**: 401 Unauthorized

**Solution**:
1. Verify you copied both Client ID and Secret correctly
2. Check for extra spaces or quotes
3. Regenerate credentials if needed
4. Ensure credentials have Fabric API access

### Issue 4: Old Token Still Referenced

**Error**: Missing EQUINIX_API_TOKEN

**Solution**:
- You're still using the old configuration
- Update to new format with Client ID and Secret
- Remove any references to `EQUINIX_API_TOKEN`

### Issue 5: Module Not Found

**Error**: No module named 'mcp'

**Solution**:
```bash
# Reinstall
pip uninstall equinix-fabric-mcp
pip install equinix-fabric-mcp

# Or install with dependencies explicitly
pip install mcp httpx
```

## 📐 Side-by-Side Comparison

| Feature | v1.0 (TypeScript) | v2.1 (Python) |
|---------|-------------------|---------------|
| Language | TypeScript/Node.js | Python 3.10+ |
| Auth | API Token | OAuth2 |
| Install | `npm install` | `pip install` |
| Config Env | `EQUINIX_API_TOKEN` | `EQUINIX_CLIENT_ID` + `EQUINIX_CLIENT_SECRET` |
| Token Refresh | Manual | Automatic |
| Token Caching | No | Yes |
| Async Support | Promise-based | Native async/await |
| Type Safety | TypeScript | Python type hints |
| Package Manager | npm | pip |
| Entry Point | `npx` / `node` | `python` / `equinix-fabric-mcp` |
| Dependencies | `@modelcontextprotocol/sdk`, `axios`, `zod` | `mcp`, `httpx` |

## 📝 Checklist

Use this checklist to track your migration:

- [ ] Verified Python 3.10+ is installed
- [ ] Uninstalled old npm package
- [ ] Installed new pip package
- [ ] Generated OAuth2 credentials
- [ ] Updated Claude Desktop config
- [ ] Removed old `EQUINIX_API_TOKEN` reference
- [ ] Added `EQUINIX_CLIENT_ID`
- [ ] Added `EQUINIX_CLIENT_SECRET`
- [ ] Restarted Claude Desktop
- [ ] Tested with simple command
- [ ] Verified all tools work
- [ ] Updated any scripts or documentation

## 📞 Support

If you encounter issues during migration:

1. Check [FAQ.md](FAQ.md) for common questions
2. Review [Troubleshooting section](QUICKSTART.md#troubleshooting)
3. Search [GitHub Issues](https://github.com/sliuuu/equinix-fabric-mcp/issues)
4. Create a new issue with:
   - Your OS and Python version
   - Error messages
   - Configuration (with secrets redacted)
   - Steps you've tried

## 🔗 Additional Resources

- [Quickstart Guide](QUICKSTART.md) - Setup from scratch
- [README](README.md) - Full documentation
- [CHANGELOG](CHANGELOG.md) - All changes in v2.1
- [Equinix API Docs](https://developer.equinix.com/docs/fabric-v4)

## ⏭️ Rolling Back

If you need to temporarily roll back to v1.0:

```bash
# Uninstall v2.1
pip uninstall equinix-fabric-mcp

# Reinstall v1.0
npm install -g equinix-fabric-mcp@1.0.0

# Revert Claude Desktop config to old format
# Restart Claude Desktop
```

**Note**: v1.0 will eventually be deprecated, so plan to migrate when ready.

---

**Migration Guide Version**: 2.1.0  
**Last Updated**: October 18, 2025  
**Need Help?**: Open an issue on GitHub
