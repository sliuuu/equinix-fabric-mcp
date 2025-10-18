# Quickstart Guide - Equinix Fabric MCP Server

Get up and running with AI-powered Equinix Fabric management in 5 minutes!

## Prerequisites

- [ ] Equinix account with Fabric access
- [ ] Claude Desktop installed
- [ ] Node.js 18+ installed
- [ ] 5 minutes of your time

## Step 1: Get Your API Token (2 minutes)

1. Go to [Equinix Fabric Portal](https://fabric.equinix.com)
2. Log in with your credentials
3. Click on your profile → **User Settings**
4. Navigate to **API** section
5. Click **Generate New Token**
6. Give it a name (e.g., "Claude MCP")
7. Copy the token immediately (you won't see it again!)
8. Save it securely

## Step 2: Install the MCP Server (1 minute)

Open your terminal and run:

```bash
npm install -g equinix-fabric-mcp
```

**That's it!** The server is now installed globally.

## Step 3: Configure Claude Desktop (2 minutes)

### Find your config file:

**macOS**: 
```bash
open ~/Library/Application\ Support/Claude/
```

**Windows**: 
```powershell
explorer %APPDATA%\Claude
```

### Edit `claude_desktop_config.json`:

If the file doesn't exist, create it. Then add:

```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "paste-your-token-here"
      }
    }
  }
}
```

**Replace `paste-your-token-here`** with your actual API token from Step 1.

### Save the file!

## Step 4: Restart Claude Desktop

Completely quit and reopen Claude Desktop for changes to take effect.

## Step 5: Test It! (30 seconds)

Open Claude Desktop and try these commands:

### Test 1: List Your Ports
```
List all my Fabric ports
```

You should see a list of your ports with details!

### Test 2: Check Connections
```
Show me all my active connections
```

### Test 3: View Metro Locations
```
What metro locations are available?
```

## 🎉 Success!

If you see results, you're all set! You can now manage Equinix Fabric using natural language.

## What Can You Do Now?

Try asking Claude:

- **"List all my Fabric resources"** - Get an overview
- **"Create a connection from Singapore to Hong Kong"** - Set up connectivity
- **"Show me my bandwidth usage"** - Monitor performance
- **"Create a cloud router in London"** - Deploy infrastructure
- **"What service profiles are available for AWS?"** - Explore cloud connections

## Common First Steps

### 1. Explore Your Infrastructure
```
Give me a summary of all my Fabric resources - ports, connections, and routers
```

### 2. Create Your First Connection
```
I want to create a 500 Mbps connection between my Singapore port and AWS. Walk me through it.
```

### 3. Set Up Multi-Cloud
```
Help me set up a cloud router in Tokyo that connects to AWS, Azure, and GCP
```

### 4. Monitor Usage
```
Show me bandwidth statistics for all my connections and identify any underutilized ones
```

## Troubleshooting

### Server Not Loading?

1. **Check Claude Desktop logs**
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

2. **Verify Node.js is installed**
   ```bash
   node --version
   ```
   Should show v18.x or higher

3. **Verify installation**
   ```bash
   npm list -g equinix-fabric-mcp
   ```

4. **Check config file syntax**
   - Ensure valid JSON (no trailing commas!)
   - Token is in quotes
   - All brackets match

### API Errors?

- **401 Unauthorized**: Double-check your API token
- **403 Forbidden**: Verify your account has Fabric API access
- **Rate Limited**: Wait a minute and try again

### Still Having Issues?

1. Check the [GitHub Issues](https://github.com/sliuuu/equinix-fabric-mcp/issues)
2. Create a new issue with:
   - Your OS and Node version
   - Error messages from Claude Desktop logs
   - Steps you've tried

## Next Steps

📚 **Learn More**:
- Read the [Usage Guide](USAGE.md) for detailed examples
- Check [Connection Examples](examples/connection-examples.md)
- Review [Router Examples](examples/router-examples.md)

🔧 **Customize**:
- Set up notifications for your connections
- Create naming conventions for your infrastructure
- Build connection templates

🚀 **Advanced**:
- Set up redundant connections
- Implement multi-cloud architectures
- Automate failover configurations

## Security Reminder

🔒 **Never share your API token!**
- Don't commit it to git
- Don't share screenshots with it visible
- Rotate it regularly
- Use separate tokens for different purposes

## Support

- 📖 [Full Documentation](README.md)
- 💬 [GitHub Discussions](https://github.com/sliuuu/equinix-fabric-mcp/discussions)
- 🐛 [Report Issues](https://github.com/sliuuu/equinix-fabric-mcp/issues)
- 🌐 [Equinix Support](https://support.equinix.com)

---

**Happy networking! 🌐**

You're now ready to manage Equinix Fabric infrastructure using AI. The network is yours to command!
