# Frequently Asked Questions (FAQ)

## General Questions

### What is the Equinix Fabric MCP Server?

It's a Model Context Protocol (MCP) server that enables AI assistants like Claude to interact with the Equinix Fabric API. This allows you to manage network infrastructure using natural language.

### Do I need programming knowledge to use this?

No! That's the beauty of MCP. You can manage your Equinix Fabric infrastructure by simply talking to Claude in natural language.

### Is this an official Equinix product?

No, this is a community-built tool that uses the official Equinix Fabric API. It's open source and maintained by the community.

### Is it free to use?

Yes, the MCP server itself is free and open source (MIT License). However, you'll pay normal Equinix Fabric fees for any resources you create or use.

## Setup & Installation

### What are the system requirements?

- **Python 3.10 or higher** (changed from Node.js in v2.1+)
- Claude Desktop application
- Equinix account with Fabric API access
- macOS, Windows, or Linux

### Where do I get OAuth2 credentials?

1. Log in to [Equinix Fabric Portal](https://fabric.equinix.com)
2. Go to **User Settings** → **API**
3. Create an **OAuth2 Application**
4. Copy both **Client ID** and **Client Secret**
5. Save them securely (never commit to version control)

### The server isn't loading in Claude Desktop. What should I check?

1. Verify your `claude_desktop_config.json` syntax is valid
2. Check that Python 3.10+ is installed: `python --version`
3. Verify the package is installed: `pip show equinix-fabric-mcp`
4. Confirm environment variables are set correctly (CLIENT_ID and CLIENT_SECRET)
5. Check Claude Desktop logs for errors
6. Restart Claude Desktop after config changes

### Can I use this with other AI assistants?

Currently, this is designed for Claude Desktop which supports MCP. As other AI assistants add MCP support, they should be able to use this server too.

## API & Permissions

### What API permissions do I need?

You need OAuth2 credentials with permissions to:
- Read Fabric resources (ports, connections, routers)
- Create/modify/delete connections
- Create/manage service tokens
- Access service profiles

**Note**: Cloud Router creation/modification requires Equinix Portal access (not available via API v4).

### Are there API rate limits?

Yes, Equinix Fabric API has rate limits. The MCP server will return errors if you hit these limits. Wait a moment and try again.

### Can I use multiple OAuth2 credentials?

You can only configure one set of credentials per MCP server instance. If you need to manage multiple accounts, you can configure multiple MCP server instances with different names.

### Is my OAuth2 secret secure?

Your credentials are stored in your local Claude Desktop config file. The server automatically handles:
- ✅ Token caching (reduces API calls)
- ✅ Automatic token refresh (improves security)
- ✅ No token persistence to disk

Never commit your config file to version control or share credentials publicly.

## Usage Questions

### What can I do with this tool?

You can:
- ✅ List and view all Fabric resources
- ✅ Create connections between ports or to cloud providers
- ✅ Manage connection bandwidth and settings
- ✅ List and view Cloud Routers (read-only in v2.2+)
- ✅ View connection status and metadata
- ✅ Search and filter resources
- ✅ Create and manage service tokens
- ❌ Create/update/delete Cloud Routers (API v4 limitation)
- ❌ Get connection statistics (API v4 limitation)

### How do I create a connection to AWS?

1. List your ports: "List my Fabric ports"
2. Find AWS service profile: "Show me AWS service profiles"
3. Ask Claude: "Create a connection from my Singapore port to AWS Direct Connect"
4. Follow Claude's guidance

### Can I automate tasks?

Yes! You can ask Claude to perform complex workflows. For example: "Create redundant connections from Singapore to Hong Kong with 1 Gbps bandwidth each"

### How do I check connection information?

"Show me details for connection [UUID]" or "List all my active connections with their current status"

**Note**: Connection statistics endpoint is deprecated in Fabric v4. Use `get_fabric_connection` for metadata instead.

## Known Limitations

### Why can't I create Cloud Routers?

**Fabric v4 API limitation** - Cloud Router create/update/delete operations are not exposed in the v4 API.

**Workaround**: Manage Cloud Routers through the [Equinix Portal](https://fabric.equinix.com). You can still LIST and VIEW existing routers via this MCP server.

### Why can't I get connection statistics?

**Fabric v4 API limitation** - The `/fabric/v4/connections/{id}/stats` endpoint is not available.

**Workaround**: Use `get_fabric_connection` to view connection metadata including state, bandwidth, and configuration details.

### What features are read-only?

In version 2.2+, the following are **read-only** due to API limitations:
- Cloud Routers (can list/view only)
- Connection Statistics (deprecated)

### Will these features be added later?

These limitations are in the Equinix Fabric v4 API itself, not the MCP server. If Equinix adds these endpoints in future API updates, we'll implement them immediately.

## Troubleshooting

### I'm getting "401 Unauthorized" errors

Your OAuth2 credentials are invalid or expired. Check:
1. Client ID is correct
2. Client Secret is correct
3. Credentials have necessary permissions
4. Generate new credentials if needed

### I'm getting "403 Forbidden" errors

Your account doesn't have the necessary permissions. Contact Equinix support to enable Fabric API access.

### I'm getting "Not supported in Fabric v4" errors

You're trying to use a feature that's not available in Fabric v4 API:
- **Cloud Router CRUD**: Use Equinix Portal instead
- **Connection Stats**: Use `get_fabric_connection` for metadata

See the [Known Limitations](#known-limitations) section above.

### I'm getting "404 Not Found" errors

The resource UUID you're trying to access doesn't exist or you don't have access to it. Double-check the UUID.

### Connections are failing to create

Check:
- Both endpoints are available
- VLANs aren't already in use
- Bandwidth is available
- Metro locations are correct
- You have sufficient permissions
- Configuration is validated before creation

### How do I view logs?

Claude Desktop logs:
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`

Look for Python errors, authentication issues, or API responses.

## Features & Capabilities

### What Fabric resources can I manage?

**Full CRUD (Create, Read, Update, Delete)**:
- ✅ Connections
- ✅ Service Tokens

**Read-Only**:
- ✅ Ports (list, view)
- ✅ Cloud Routers (list, view) - v4 API limitation
- ✅ Service Profiles (list, view)
- ✅ Metro Locations (list)

**Not Available**:
- ❌ Cloud Router CRUD - API v4 limitation (use Portal)
- ❌ Connection Statistics - API v4 limitation
- ❌ Route Filters - Not yet in v4 API

### Can I create redundant connections?

Yes! You can create connection pairs with redundancy configuration. See [README examples](README.md#usage-examples) for details.

### Can I connect to multiple cloud providers?

Absolutely! Create connections to AWS, Azure, GCP, Oracle Cloud, IBM Cloud, and more. 

**Note**: Multi-cloud connectivity via Cloud Routers requires creating the router through the Equinix Portal first, then creating connections to it.

### Does it support BGP configuration?

BGP configuration is managed through Equinix Portal or Cloud Router management interfaces, not this MCP server.

### Can I monitor connection health?

You can view connection status and metadata through `get_fabric_connection`. For detailed monitoring, use Equinix's monitoring tools or integrate with your existing monitoring stack.

## Cost & Billing

### Does this cost extra?

No, the MCP server is free. You only pay standard Equinix Fabric fees for the resources you provision.

### Will I be charged for API calls?

No, Equinix Fabric API calls are free. You're only charged for active resources (ports, connections, routers).

### How can I estimate costs?

Consult Equinix pricing documentation or contact Equinix sales. The MCP server can help you provision resources but doesn't provide pricing information.

### Can I set spending limits?

Spending limits are managed through your Equinix account, not through this MCP server.

## Development & Contributing

### How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Contributions are welcome!

### Can I add support for new API endpoints?

Yes! Check the [Equinix Fabric API docs](https://developer.equinix.com/docs/fabric-v4), add the tool definition and handler to `server.py`, and submit a PR.

### Where should I report bugs?

[GitHub Issues](https://github.com/sliuuu/equinix-fabric-mcp/issues)

### Can I fork this for my own needs?

Yes! It's MIT licensed, so you can fork, modify, and use it as needed.

## Security

### Is my data secure?

Your OAuth2 credentials are stored locally on your machine. API calls go directly from your machine to Equinix's API servers. No data passes through any third-party servers.

The server uses OAuth2 Client Credentials flow which is more secure than static API tokens:
- ✅ Short-lived access tokens
- ✅ Automatic token refresh
- ✅ No persistent token storage
- ✅ Fine-grained permission control

### Should I rotate my OAuth2 credentials?

Yes, as a security best practice, rotate your credentials regularly (e.g., every 90 days).

### What if my credentials are compromised?

1. Immediately revoke them in the Equinix Portal
2. Generate new OAuth2 credentials
3. Update your Claude Desktop config
4. Review recent activity for any unauthorized changes

### Can I use this in a CI/CD pipeline?

While possible, this tool is designed for interactive use with Claude. For automation, consider using the Equinix Fabric API directly with the official Python SDK.

## Advanced Usage

### Can I manage multiple Equinix accounts?

Yes, configure multiple MCP server instances with different credentials:

```json
{
  "mcpServers": {
    "equinix-prod": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "EQUINIX_CLIENT_ID": "prod-client-id",
        "EQUINIX_CLIENT_SECRET": "prod-client-secret"
      }
    },
    "equinix-dev": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "EQUINIX_CLIENT_ID": "dev-client-id",
        "EQUINIX_CLIENT_SECRET": "dev-client-secret"
      }
    }
  }
}
```

### Can I use this with the n8n MCP server?

Yes! You can configure multiple MCP servers simultaneously. For example, use n8n MCP for workflow automation and Equinix Fabric MCP for network management.

### How do I update to the latest version?

```bash
pip install --upgrade equinix-fabric-mcp
```

Then restart Claude Desktop.

### What changed between v1.0 and v2.x?

- **Language**: TypeScript → Python 3.10+
- **Auth**: Static API token → OAuth2 Client Credentials
- **Installation**: npm → pip
- **Config**: Different environment variables

See [MIGRATION.md](MIGRATION.md) for details.

## Version Information

### What version am I running?

Check your installed version:
```bash
pip show equinix-fabric-mcp
```

Latest version: **2.2.0** (October 20, 2025)

### What's new in v2.2?

- ✅ Accurate documentation of API v4 limitations
- ✅ Clear error messages for unsupported operations
- ✅ Updated Known Limitations section
- ✅ Improved troubleshooting guides
- 📄 Documentation-only update (no code changes)

### Should I upgrade from v2.1 to v2.2?

Yes, but it's not urgent - v2.2 is a documentation update only. Your existing v2.1 installation continues to work identically. Upgrading gives you:
- More accurate documentation
- Better understanding of API limitations
- Improved troubleshooting information

## Still Have Questions?

- 📖 [Full Documentation](README.md)
- 🚀 [Quickstart Guide](QUICKSTART.md)
- 📋 [Changelog](CHANGELOG.md)
- 💬 [GitHub Discussions](https://github.com/sliuuu/equinix-fabric-mcp/discussions)
- 🐛 [Report an Issue](https://github.com/sliuuu/equinix-fabric-mcp/issues)
- 🌐 [Equinix Support](https://support.equinix.com)
