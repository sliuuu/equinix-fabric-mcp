# Contributing to Equinix Fabric MCP Server

Thank you for your interest in contributing to the Equinix Fabric MCP Server! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/sliuuu/equinix-fabric-mcp/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Node version, etc.)
   - Error messages or logs

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear use case description
   - Expected behavior
   - Why this would be useful
   - Potential implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/sliuuu/equinix-fabric-mcp.git
   cd equinix-fabric-mcp
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   npm install
   npm run build
   npm run dev
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   Use conventional commit messages:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Test additions/changes
   - `chore:` - Build process or auxiliary tool changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Include screenshots if UI changes

## Development Setup

### Prerequisites

- Node.js 18.x or 20.x
- npm or yarn
- Git
- Equinix API token for testing

### Local Development

```bash
# Clone repository
git clone https://github.com/sliuuu/equinix-fabric-mcp.git
cd equinix-fabric-mcp

# Install dependencies
npm install

# Build
npm run build

# Watch mode for development
npm run watch

# Run in development mode
export EQUINIX_API_TOKEN="your-token"
npm run dev
```

## Project Structure

```
equinix-fabric-mcp/
├── src/
│   └── index.ts          # Main MCP server implementation
├── dist/                 # Compiled JavaScript (generated)
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── README.md             # Main documentation
├── USAGE.md              # Usage guide
├── CONTRIBUTING.md       # This file
└── LICENSE               # MIT License
```

## Code Style

- Use TypeScript for all source code
- Follow existing formatting conventions
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

## Testing

Currently, the project uses manual testing. Contributions to add automated tests are welcome!

### Manual Testing Checklist

- [ ] All tools load correctly
- [ ] API authentication works
- [ ] List operations return data
- [ ] Get operations retrieve specific resources
- [ ] Create operations succeed with valid input
- [ ] Update operations modify resources correctly
- [ ] Delete operations remove resources
- [ ] Error handling works properly
- [ ] Rate limiting is respected

## Adding New Tools

1. **Define the tool** in the `tools` array:
   ```typescript
   {
     name: 'your_tool_name',
     description: 'Clear description of what it does',
     inputSchema: {
       type: 'object',
       properties: {
         // Define parameters
       },
       required: ['required_params'],
     },
   }
   ```

2. **Implement the handler** in the `CallToolRequestSchema` handler:
   ```typescript
   case 'your_tool_name': {
     const { param1, param2 } = args as any;
     const response = await apiClient.get('/fabric/v4/endpoint');
     return {
       content: [
         {
           type: 'text',
           text: JSON.stringify(response.data, null, 2),
         },
       ],
     };
   }
   ```

3. **Update documentation** in README.md and USAGE.md

4. **Test thoroughly** with various inputs

## API Coverage

We aim to support the full Equinix Fabric API. Priority areas:

- ✅ Ports (list, get)
- ✅ Connections (list, get, create, update, delete, stats)
- ✅ Routers (list, get, create, update, delete)
- ✅ Service Profiles (list, get)
- ✅ Service Tokens (list, get, create, delete)
- ✅ Metros (list)
- ⬜ Network operations
- ⬜ Route filters
- ⬜ Pricing
- ⬜ Usage statistics

## Documentation

Good documentation is crucial. When contributing:

- Update README.md for new features
- Add usage examples to USAGE.md
- Include inline code comments
- Update API coverage list
- Add troubleshooting tips if applicable

## Release Process

1. Update version in package.json
2. Update CHANGELOG.md
3. Create git tag
4. Push to GitHub
5. Publish to npm (maintainers only)

## Getting Help

If you need help:

- Open a [Discussion](https://github.com/sliuuu/equinix-fabric-mcp/discussions)
- Ask in the issue comments
- Check existing documentation

## Recognition

All contributors will be recognized in:
- GitHub contributors list
- Release notes
- Project documentation

Thank you for contributing to making network automation more accessible through AI!
