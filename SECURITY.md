# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Best Practices

### API Token Management

#### ✅ DO

- Store tokens in environment variables or secure config files
- Use separate tokens for different environments (dev/staging/prod)
- Rotate tokens regularly (recommended: every 90 days)
- Revoke tokens immediately if compromised
- Use tokens with minimal required permissions
- Keep token access restricted to necessary personnel

#### ❌ DON'T

- Never commit tokens to version control
- Never share tokens via email or chat
- Never log tokens in application logs
- Never include tokens in screenshots or recordings
- Never use production tokens in development
- Never share tokens across multiple people

### Configuration Security

#### Secure Config File Permissions

**macOS/Linux**:
```bash
chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**:
- Right-click config file → Properties
- Security tab → Advanced
- Remove all users except yourself

#### Config File Template

```json
{
  "mcpServers": {
    "equinix-fabric": {
      "command": "npx",
      "args": ["-y", "equinix-fabric-mcp"],
      "env": {
        "EQUINIX_API_TOKEN": "REPLACE_WITH_YOUR_TOKEN"
      }
    }
  }
}
```

### Network Security

#### TLS/HTTPS

- All API calls use HTTPS (TLS 1.2+)
- Certificate validation is enabled
- No plaintext transmission of credentials

#### Firewall Configuration

Allow outbound HTTPS to:
- `api.equinix.com` (443)
- `registry.npmjs.org` (443) - for installation only

### Application Security

#### Dependency Security

- Regular dependency updates
- Automated vulnerability scanning
- Use of trusted packages only

#### Input Validation

- All user inputs are validated
- API parameters are type-checked
- Schema validation with Zod

### Least Privilege Access

#### API Token Permissions

Create tokens with minimum required permissions:

- **Read-only token**: For monitoring and reporting
- **Standard token**: For normal operations
- **Admin token**: Only when necessary

#### Recommended Permission Sets

**Development**:
- Read: Ports, Connections, Routers
- Write: Test environment only

**Production**:
- Read: All resources
- Write: Connections, Routers (with approval)
- Delete: Restricted or disabled

## Reporting a Vulnerability

### How to Report

If you discover a security vulnerability, please report it by:

1. **DO NOT** open a public GitHub issue
2. Email: [Create a private security advisory on GitHub](https://github.com/sliuuu/equinix-fabric-mcp/security/advisories/new)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 7 days
  - High: 30 days
  - Medium: 90 days
  - Low: Next release

### Disclosure Policy

- We practice responsible disclosure
- Security fixes are released ASAP
- CVE IDs assigned for serious vulnerabilities
- Public disclosure after fix is available
- Reporter credited (unless they prefer anonymity)

## Security Features

### Current Implementation

- ✅ HTTPS/TLS for all API communication
- ✅ Bearer token authentication
- ✅ No credential storage in code
- ✅ Environment variable configuration
- ✅ Input validation
- ✅ Error message sanitization
- ✅ Dependency vulnerability scanning

### Planned Enhancements

- ⏳ Token encryption at rest
- ⏳ Audit logging
- ⏳ Rate limiting
- ⏳ Request signing
- ⏳ Two-factor authentication support

## Incident Response

### If Your Token is Compromised

1. **Immediately**:
   - Revoke the token in Equinix Portal
   - Generate a new token
   - Update your configuration

2. **Within 24 hours**:
   - Review API access logs
   - Check for unauthorized changes
   - Document the incident

3. **Follow-up**:
   - Implement additional controls
   - Review access policies
   - Update security procedures

### Detection Indicators

 Watch for:
- Unexpected API calls
- Unauthorized resource creation
- Changes to critical resources
- Unusual access patterns
- Failed authentication attempts

## Compliance

### Data Handling

- No PII collected by MCP server
- No data persistence
- No third-party data sharing
- API responses pass through only

### Audit Trail

- Equinix maintains API access logs
- Claude Desktop logs available locally
- Review logs regularly

## Security Checklist

### Before Deployment

- [ ] API token generated with minimal permissions
- [ ] Config file permissions restricted
- [ ] Token not in version control
- [ ] HTTPS enforced for all connections
- [ ] Dependencies updated to latest secure versions

### Regular Maintenance

- [ ] Rotate API tokens every 90 days
- [ ] Review access logs monthly
- [ ] Update dependencies monthly
- [ ] Review and update permissions quarterly
- [ ] Conduct security review annually

### Incident Preparation

- [ ] Document token revocation procedure
- [ ] Identify incident response contacts
- [ ] Maintain backup access methods
- [ ] Test token rotation process

## Secure Development

### Code Review Guidelines

- Review all code for security issues
- Check for credential leaks
- Validate input handling
- Verify error message safety
- Ensure proper auth checks

### Testing Requirements

- Test with invalid tokens
- Test with insufficient permissions
- Test error handling
- Test input validation
- Test rate limiting behavior

## Third-Party Security

### Dependencies

We use:
- `@modelcontextprotocol/sdk` - Official MCP implementation
- `axios` - Widely used, regularly updated
- `zod` - Security-focused validation

### Supply Chain Security

- Dependencies pinned in package.json
- Regular security audits with `npm audit`
- Automated dependency updates
- Source code review for major updates

## Contact

For security concerns:
- GitHub Security Advisories: [Create Advisory](https://github.com/sliuuu/equinix-fabric-mcp/security/advisories/new)
- General Security Questions: Open a [Discussion](https://github.com/sliuuu/equinix-fabric-mcp/discussions)

## Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities.

---

**Last Updated**: October 18, 2025
**Next Review**: January 18, 2026
