# Deployment Guide

Complete guide for deploying and managing the Equinix Fabric MCP Server.

## Prerequisites Check

Before deploying, ensure you have:

- [ ] Node.js 18.x or 20.x installed
- [ ] npm or yarn package manager
- [ ] Claude Desktop application
- [ ] Equinix account with Fabric access
- [ ] Equinix API token
- [ ] Terminal/command line access

## Deployment Methods

### Method 1: NPM Global Installation (Recommended)

#### Advantages
- Simple one-command installation
- Automatic updates available
- Works across all projects
- No manual build required

#### Steps

1. **Install globally**:
```bash
npm install -g equinix-fabric-mcp
```

2. **Verify installation**:
```bash
which equinix-fabric-mcp  # macOS/Linux
where equinix-fabric-mcp  # Windows
```

3. **Configure Claude Desktop**:

Edit config file at:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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

4. **Restart Claude Desktop**

5. **Test**:
```
Ask Claude: "List my Fabric ports"
```

### Method 2: Local Development Installation

#### Advantages
- Full source code access
- Can make custom modifications
- Latest development features
- Useful for contributing

#### Steps

1. **Clone repository**:
```bash
git clone https://github.com/sliuuu/equinix-fabric-mcp.git
cd equinix-fabric-mcp
```

2. **Install dependencies**:
```bash
npm install
```

3. **Build**:
```bash
npm run build
```

4. **Configure Claude Desktop**:
```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "node",
      "args": ["/full/path/to/equinix-fabric-mcp/dist/index.js"],
      "env": {
        "EQUINIX_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

5. **Restart Claude Desktop**

### Method 3: Docker Deployment (Future)

*Coming soon - Docker container for isolated deployment*

## Multi-Environment Setup

### Managing Multiple Environments

Configure separate instances for different environments:

```json
{
  "mcpServers": {
    "equinix-production": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "prod-token-here"
      }
    },
    "equinix-staging": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "staging-token-here"
      }
    },
    "equinix-development": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "dev-token-here"
      }
    }
  }
}
```

Then in Claude:
```
"Using equinix-production, list my connections"
"Using equinix-staging, create a test connection"
```

## Environment Variable Management

### Option 1: Direct in Config (Simple)

```json
{
  "env": {
    "EQUINIX_API_TOKEN": "your-token"
  }
}
```

### Option 2: Shell Environment Variables (Secure)

1. Add to shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export EQUINIX_API_TOKEN="your-token"
```

2. Update config to reference:
```json
{
  "env": {
    "EQUINIX_API_TOKEN": "${EQUINIX_API_TOKEN}"
  }
}
```

### Option 3: Secrets Management (Production)

For production deployments:
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- 1Password CLI

Example with 1Password:
```bash
export EQUINIX_API_TOKEN=$(op read "op://Private/Equinix/token")
```

## Update Procedures

### Updating Global Installation

```bash
# Check current version
npm list -g equinix-fabric-mcp

# Update to latest
npm update -g equinix-fabric-mcp

# Or install specific version
npm install -g equinix-fabric-mcp@1.0.0

# Restart Claude Desktop
```

### Updating Local Installation

```bash
cd equinix-fabric-mcp

# Pull latest changes
git pull origin main

# Update dependencies
npm install

# Rebuild
npm run build

# Restart Claude Desktop
```

## Verification & Testing

### Post-Deployment Checklist

1. **Server Loading**:
   - [ ] No errors in Claude Desktop logs
   - [ ] MCP server appears in tools list

2. **Basic Operations**:
   - [ ] List ports works
   - [ ] List connections works
   - [ ] Get specific resource works

3. **API Connectivity**:
   - [ ] API authentication succeeds
   - [ ] Resources load correctly
   - [ ] Error handling works

### Test Commands

```
# Test 1: List Operations
"List all my Fabric ports"
"Show me all my connections"
"List available metros"

# Test 2: Get Operations
"Show me details about port [UUID]"
"Get connection information for [UUID]"

# Test 3: Search
"Find all active connections"
"Show me service profiles for AWS"

# Test 4: Stats
"What's the bandwidth usage on connection [UUID]?"
```

## Troubleshooting Deployment

### Issue: Server Not Loading

**Symptoms**: No Equinix tools available in Claude

**Solutions**:
1. Check Node.js version: `node --version`
2. Verify installation: `npm list -g equinix-fabric-mcp`
3. Check config file syntax (valid JSON)
4. Review Claude Desktop logs
5. Restart Claude Desktop

### Issue: Authentication Failures

**Symptoms**: 401 errors, "Unauthorized" messages

**Solutions**:
1. Verify API token is correct
2. Check token hasn't expired
3. Ensure token has necessary permissions
4. Regenerate token if needed

### Issue: Missing Dependencies

**Symptoms**: Module not found errors

**Solutions**:
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Issue: Permission Errors

**Symptoms**: Cannot access config file or directories

**Solutions**:
```bash
# Fix config file permissions (macOS/Linux)
chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
```

## Monitoring

### Log Locations

**Claude Desktop Logs**:
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`

**View Recent Logs**:
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Windows
Get-Content $env:APPDATA\Claude\logs\mcp*.log -Wait
```

### Health Checks

Regularly verify:
- Server is responding
- API connectivity works
- No error patterns in logs
- Response times are acceptable

## Backup & Recovery

### Backup Configuration

```bash
# Backup Claude Desktop config
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/claude_config_backup.json
```

### Recovery Procedure

1. **Reinstall Package**:
```bash
npm uninstall -g equinix-fabric-mcp
npm install -g equinix-fabric-mcp
```

2. **Restore Configuration**:
```bash
cp ~/claude_config_backup.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

3. **Restart Claude Desktop**

## Security Hardening

### File Permissions

```bash
# Secure config file (macOS/Linux)
chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Verify
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Should show: -rw------- (600)
```

### Token Rotation Schedule

1. Generate new token in Equinix Portal
2. Test new token with test account/environment
3. Update production configuration
4. Restart Claude Desktop
5. Verify functionality
6. Revoke old token

**Recommended Schedule**: Every 90 days

## Performance Optimization

### Connection Pooling (Future)

Currently not implemented, but planned for future releases.

### Caching Strategy

Claude may cache some responses. For fresh data:
```
"Refresh my connection list"
"Get the latest status for connection [UUID]"
```

## Uninstallation

### Remove Global Installation

```bash
# Uninstall package
npm uninstall -g equinix-fabric-mcp

# Remove from Claude config
# Edit claude_desktop_config.json and remove equinix-fabric section

# Restart Claude Desktop
```

### Remove Local Installation

```bash
# Remove directory
cd ..
rm -rf equinix-fabric-mcp

# Remove from Claude config
# Edit claude_desktop_config.json

# Restart Claude Desktop
```

## Migration Guide

### From Local to Global Installation

1. **Note your current config**
2. **Install globally**:
```bash
npm install -g equinix-fabric-mcp
```
3. **Update Claude config**:
```json
{
  "command": "npx",
  "args": ["-y", "equinix-fabric-mcp"]
}
```
4. **Test and verify**
5. **Remove local installation** (optional)

### From Global to Local Installation

1. **Clone repository**
2. **Build locally**
3. **Update Claude config** with full path
4. **Test and verify**
5. **Uninstall global** (optional)

## Best Practices

### Development
- Use local installation
- Keep on latest commit
- Use dev environment tokens
- Test before deploying

### Staging
- Use global installation
- Pin to specific version
- Use staging tokens
- Mirror production config

### Production
- Use global installation
- Pin to stable version
- Use production tokens
- Secure configuration files
- Regular token rotation
- Monitor logs
- Schedule updates

## Support Resources

### Documentation
- [README](README.md) - Overview and features
- [QUICKSTART](QUICKSTART.md) - Quick setup guide
- [USAGE](USAGE.md) - Detailed usage examples
- [FAQ](FAQ.md) - Common questions
- [SECURITY](SECURITY.md) - Security guidelines
- [ARCHITECTURE](ARCHITECTURE.md) - Technical details

### Getting Help
- [GitHub Issues](https://github.com/sliuuu/equinix-fabric-mcp/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/sliuuu/equinix-fabric-mcp/discussions) - Questions and discussions
- [Equinix Support](https://support.equinix.com) - Equinix API issues

## Deployment Checklist

### Pre-Deployment
- [ ] Node.js 18+ installed
- [ ] Claude Desktop installed
- [ ] Equinix API token generated
- [ ] Permissions verified
- [ ] Network access confirmed

### During Deployment
- [ ] Package installed successfully
- [ ] Configuration file created
- [ ] Token added securely
- [ ] File permissions set
- [ ] Claude Desktop restarted

### Post-Deployment
- [ ] Server loads without errors
- [ ] Basic commands work
- [ ] API authentication succeeds
- [ ] Resources accessible
- [ ] Performance acceptable
- [ ] Documentation reviewed
- [ ] Team trained (if applicable)

## Maintenance Schedule

### Daily
- Monitor for errors in logs
- Verify service availability

### Weekly
- Review usage patterns
- Check for updates

### Monthly
- Update to latest version
- Review and optimize configuration
- Check for security advisories

### Quarterly
- Rotate API tokens
- Review access permissions
- Audit usage and costs
- Update documentation

---

**Deployment Guide Version**: 1.0.0  
**Last Updated**: October 18, 2025  
**Next Review**: January 18, 2026
