# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-18

### Added
- Initial release of Equinix Fabric MCP Server
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

### Features

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

### Developer Experience
- TypeScript support with type definitions
- Watch mode for development
- Build and prepare scripts
- Comprehensive inline documentation

### Documentation
- Complete README with installation and setup
- Detailed USAGE guide with examples
- Contributing guidelines
- MIT License
- Changelog (this file)

## [Unreleased]

### Planned
- Route filter management
- Network operations support
- Pricing information tools
- Enhanced usage statistics
- Automated testing suite
- Multi-region support enhancements
- Batch operations
- Webhook support
- Advanced monitoring tools

### Under Consideration
- GraphQL support
- Connection templates
- Cost optimization recommendations
- Automated failover management
- Integration with other MCP servers
- Connection health monitoring
- Performance analytics

---

## Version History

- **1.0.0** - Initial public release with core functionality

## Upgrade Guide

### To 1.0.0
This is the initial release. Follow the installation instructions in README.md.

## Breaking Changes

None yet - this is the initial release.

## Deprecations

None yet - this is the initial release.

## Security

- Always use environment variables for API tokens
- Never commit tokens to version control
- Rotate API tokens regularly
- Follow principle of least privilege

For security issues, please email security@example.com or create a private security advisory on GitHub.
