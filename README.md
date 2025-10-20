# Unofficial Equinix Fabric MCP Server v2.2

**Python implementation** - A Model Context Protocol (MCP) server that provides AI assistants with tools to interact with the Equinix Fabric API. This enables AI-powered management of network connections, ports, routers, and service profiles.

## 🚀 Features

### Port Management
- List all Fabric ports in your account
- Get detailed information about specific ports

### Connection Management
- List all Fabric connections
- Get detailed connection information
- **Create new virtual connections** between endpoints
- **Update existing connections** (bandwidth, name, description)
- **Delete connections**
- ~~Get connection statistics~~ (deprecated in Fabric v4)
- Search connections by filters
- Validate connection configurations before creation

### Cloud Router Management
- List all Fabric Cloud Routers
- Get detailed router information
- ⚠️ **Note**: Create/Update/Delete operations are not supported in the current Fabric MCP server

### Service Profiles & Tokens
- List available service profiles (cloud providers and partners)
- Get service profile details
- **Create and manage service tokens** for partner connections
- List and delete service tokens

### Metro Locations
- List all available Equinix Fabric metro locations

## 📋 Prerequisites

- Python 3.10 or higher
- Claude Desktop application
- Equinix account with Fabric API access
- Equinix OAuth2 credentials (Client ID and Client Secret)

## 🔧 Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip install equinix-fabric-mcp
```

### Method 2: Install from Source

```bash
git clone https://github.com/sliuuu/equinix-fabric-mcp.git
cd equinix-fabric-mcp
pip install -e .
```

## ⚙️ Configuration

### Step 1: Get Your Equinix API Credentials

1. Log in to the [Equinix Fabric Portal](https://fabric.equinix.com)
2. Navigate to **User Settings** → **API**
3. Create an OAuth2 application to get:
   - **Client ID**
   - **Client Secret**
4. Save these credentials securely

### Step 2: Configure Claude Desktop

Edit your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "EQUINIX_CLIENT_ID": "your-client-id-here",
        "EQUINIX_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

**Or if installed via pip:**

```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "equinix-fabric-mcp",
      "env": {
        "EQUINIX_CLIENT_ID": "your-client-id-here",
        "EQUINIX_CLIENT_SECRET": "your-client-secret-here"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop

Completely quit and reopen Claude Desktop for changes to take effect.

## 💡 Usage Examples

Once configured, you can ask Claude to help with Equinix Fabric tasks:

### Read Operations
```
"List all my Fabric ports"
"Show me details about port [UUID]"
"List all my connections"
"Show me available service profiles for AWS"
"List all metros in Asia"
"Search for connections with state ACTIVE"
```

### Write Operations
```
"Create a connection between my Singapore port and AWS Direct Connect"
"Update connection [UUID] to 1000 Mbps bandwidth"
"Delete connection [UUID]"
"Create a service token for my Hong Kong port"
"Validate this connection configuration before creating it"
```

### Complex Workflows
```
"Set up redundant connections from Singapore to Tokyo"
"Create a multi-cloud hub in New York connecting to AWS, Azure, and GCP"
"Show me all ACTIVE connections and their bandwidth usage"
```

## 🔐 Authentication

This server uses **OAuth2 Client Credentials** flow for authentication:

- Access tokens are automatically obtained and cached
- Tokens are refreshed automatically before expiration (1 minute buffer)
- More secure than API key authentication
- Supports fine-grained permission control

## 🛠️ Available Tools

The server provides **22 MCP tools**:

### Read Operations (9 tools)
1. `list_fabric_ports` - List all ports
2. `get_fabric_port` - Get port details
3. `list_fabric_connections` - List connections
4. `get_fabric_connection` - Get connection details
5. ~~`get_connection_stats`~~ - **Deprecated** (not supported in Fabric v4)
6. `list_fabric_routers` - List Cloud Routers
7. `get_fabric_router` - Get router details
8. `search_connections` - Search with filters
9. `list_metros` - List metro locations

### Connection Management (4 tools)
10. `create_fabric_connection` - Create new connections
11. `update_connection` - Modify connections
12. `delete_connection` - Remove connections
13. `validate_connection_config` - Pre-validate configs

### Cloud Router Management (3 tools) ⚠️ **READ-ONLY**
14. ~~`create_fabric_router`~~ - **Not supported in Fabric v4 API**
15. ~~`update_fabric_router`~~ - **Not supported in Fabric v4 API**
16. ~~`delete_fabric_router`~~ - **Not supported in Fabric v4 API**

> **⚠️ Important**: Cloud Router create/update/delete operations are not available in Fabric v4 API. You can only LIST and GET existing routers. Cloud Routers must be managed through the Equinix Portal or alternative methods.

### Service Profiles (2 tools)
17. `list_service_profiles` - Browse cloud providers
18. `get_service_profile` - Get profile details

### Service Tokens (4 tools)
19. `create_service_token` - Generate access tokens
20. `list_service_tokens` - List all tokens
21. `get_service_token` - Get token details
22. `delete_service_token` - Revoke tokens

## 📚 API Coverage

This MCP server implements the Equinix Fabric API v4:

- **Ports**: GET /fabric/v4/ports
- **Connections**: GET, POST, PATCH, DELETE /fabric/v4/connections
- **Cloud Routers**: GET /fabric/v4/routers (search endpoint, read-only)
- **Service Profiles**: GET /fabric/v4/serviceProfiles
- **Service Tokens**: GET, POST, DELETE /fabric/v4/serviceTokens
- **Metros**: GET /fabric/v4/metros
- **Search**: POST /fabric/v4/connections/search, POST /fabric/v4/routers/search

### Known API Limitations

- ❌ **Connection Statistics**: `/fabric/v4/connections/{id}/stats` endpoint not available in v4 
- ❌ **Cloud Router CRUD**: POST/PATCH/DELETE operations not available in v4 API
- ✅ **Workaround**: Use `get_fabric_connection` for connection metadata
- ✅ **Workaround**: Manage Cloud Routers through Equinix Portal

## 🔍 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/sliuuu/equinix-fabric-mcp.git
cd equinix-fabric-mcp

# Install with dev dependencies
pip install -e ".[dev]"

# Set environment variables
export EQUINIX_CLIENT_ID="your-client-id"
export EQUINIX_CLIENT_SECRET="your-client-secret"

# Run the server
python -m server
```

### Code Quality

```bash
# Format code
black server.py

# Type checking
mypy server.py

# Run tests (when available)
pytest
```

## 🆚 Version 2.2 Updates

### New in v2.2
- ✅ **Accurate API v4 implementation** - Properly documents unsupported endpoints
- ✅ **Clear error messages** - NotImplementedError for unsupported operations
- ✅ **Cloud Router read operations** - List and get router details via search
- ✅ **Updated documentation** - Reflects actual Fabric v4 API capabilities

### New in v2.1
- ✅ **OAuth2 authentication** (more secure than API keys)
- ✅ **Token caching** (improved performance)
- ✅ **Python 3.10+ support**
- ✅ **Async/await throughout**
- ✅ **Better error handling**
- ✅ **Comprehensive tool schemas**

### Migrating from v1.x
- Authentication changed from Bearer token to OAuth2
- Environment variables changed:
  - Old: `EQUINIX_API_TOKEN`
  - New: `EQUINIX_CLIENT_ID` + `EQUINIX_CLIENT_SECRET`
- All functionality preserved and enhanced

## 🔒 Security

### Best Practices

- ✅ Never commit credentials to version control
- ✅ Use environment variables for secrets
- ✅ Rotate OAuth2 credentials regularly
- ✅ Use least-privilege access
- ✅ Review API access logs periodically

### Secure Configuration

```bash
# macOS/Linux - Set file permissions
chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Use secret management tools
export EQUINIX_CLIENT_ID=$(op read "op://Private/Equinix/client_id")
export EQUINIX_CLIENT_SECRET=$(op read "op://Private/Equinix/client_secret")
```

## 🐛 Troubleshooting

### Server Not Loading

1. Check Python version: `python --version` (requires 3.10+)
2. Verify installation: `pip show equinix-fabric-mcp`
3. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`
4. Validate JSON syntax in config file
5. Restart Claude Desktop

### Authentication Errors

- **401 Unauthorized**: Check client ID and secret are correct
- **403 Forbidden**: Verify account has Fabric API access
- **Token expired**: Server auto-refreshes, but check credentials

### Connection Issues

- Verify both endpoints exist and are available
- Check VLAN tags aren't already in use
- Ensure bandwidth is available in the metro
- Validate metro codes match service requirements

### API Limitation Errors

- **"Not supported in Fabric v4"**: Operation unavailable - see Known API Limitations section
- **Connection stats unavailable**: Use `get_fabric_connection` for metadata instead
- **Cloud Router creation fails**: Manage Cloud Routers through Equinix Portal

## 📖 Documentation

- [Quickstart Guide](QUICKSTART.md) - Get started in 5 minutes
- [Usage Guide](USAGE.md) - Detailed examples
- [FAQ](FAQ.md) - Common questions
- [Security Guide](SECURITY.md) - Security best practices
- [Architecture](ARCHITECTURE.md) - Technical details
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Deployment Guide](DEPLOYMENT.md) - Production deployment

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **GitHub Issues**: https://github.com/sliuuu/equinix-fabric-mcp/issues
- **Discussions**: https://github.com/sliuuu/equinix-fabric-mcp/discussions
- **Equinix Support**: https://support.equinix.com

## 🔗 Resources

- [Equinix Fabric API Documentation](https://developer.equinix.com/docs/fabric-v4)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Claude Desktop](https://claude.ai/desktop)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Version**: 2.2  
**Last Updated**: October 20, 2025  

**Language**: Python 3.10+
