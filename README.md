# Equinix Fabric MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with tools to interact with the Equinix Fabric API. This enables AI-powered management of network connections, ports, routers, and service profiles.

## Features

### Port Management
- List all Fabric ports in your account
- Get detailed information about specific ports

### Connection Management
- List all Fabric connections
- Get detailed connection information
- Create new virtual connections between endpoints
- Update existing connections (bandwidth, name, description)
- Delete connections
- Get connection statistics (bandwidth, traffic)
- Search connections by filters
- Validate connection configurations before creation

### Cloud Router Management
- List all Fabric Cloud Routers
- Get detailed router information
- Create new Cloud Routers with BGP support
- Update router configurations
- Delete routers

### Service Profiles & Tokens
- List available service profiles (cloud providers and partners)
- Get service profile details
- Create and manage service tokens for partner connections

### Metro Locations
- List all available Equinix Fabric metro locations

## Installation

```bash
npm install -g equinix-fabric-mcp
```

Or install locally:

```bash
git clone https://github.com/sliuuu/equinix-fabric-mcp.git
cd equinix-fabric-mcp
npm install
npm run build
```

## Configuration

### Environment Variables

You need to set your Equinix API credentials:

```bash
export EQUINIX_API_TOKEN="your-api-token-here"
```

To get your API token:
1. Log in to the Equinix Fabric Portal
2. Navigate to API Settings
3. Generate a new API token

### Claude Desktop Configuration

Add to your Claude Desktop config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

Or if installed locally:

```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "node",
      "args": ["/path/to/equinix-fabric-mcp/dist/index.js"],
      "env": {
        "EQUINIX_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

## Usage Examples

Once configured, you can ask Claude to help with Equinix Fabric tasks:

- "List all my Fabric ports"
- "Show me details about port [UUID]"
- "Create a connection between my port in Singapore and AWS Direct Connect"
- "What's the bandwidth usage on connection [UUID]?"
- "List all my active connections"
- "Create a Cloud Router in London with PRO package"
- "Show me available service profiles for Azure"

## API Coverage

This MCP server implements the following Equinix Fabric API endpoints:

- **Ports**: GET /fabric/v4/ports, GET /fabric/v4/ports/{portId}
- **Connections**: GET /fabric/v4/connections, POST /fabric/v4/connections, GET /fabric/v4/connections/{connectionId}, PATCH /fabric/v4/connections/{connectionId}, DELETE /fabric/v4/connections/{connectionId}
- **Routers**: GET /fabric/v4/routers, POST /fabric/v4/routers, GET /fabric/v4/routers/{routerId}, PATCH /fabric/v4/routers/{routerId}, DELETE /fabric/v4/routers/{routerId}
- **Service Profiles**: GET /fabric/v4/serviceProfiles
- **Service Tokens**: GET /fabric/v4/serviceTokens, POST /fabric/v4/serviceTokens
- **Metros**: GET /fabric/v4/metros
- **Statistics**: GET /fabric/v4/connections/{connectionId}/stats

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Watch mode for development
npm run watch

# Run in development mode
npm run dev
```

## Security

- Never commit your API token to version control
- Use environment variables or secure secret management
- Review the principle of least privilege for API tokens
- Rotate tokens regularly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/sliuuu/equinix-fabric-mcp/issues
- Equinix Support: https://support.equinix.com

## Resources

- [Equinix Fabric API Documentation](https://developer.equinix.com/docs/fabric-v4)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Claude Desktop Documentation](https://claude.ai/desktop)
