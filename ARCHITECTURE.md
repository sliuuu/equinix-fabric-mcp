# Architecture Documentation

## Overview

The Equinix Fabric MCP Server is a TypeScript-based implementation of the Model Context Protocol (MCP) that bridges AI assistants with the Equinix Fabric API.

## System Architecture

```
┌────────────────────┐
│   Claude Desktop   │
│  (AI Assistant)    │
└─────────┬──────────┘
         │ MCP Protocol
         │ (stdio)
         │
┌─────────┴──────────────────────────┐
│   Equinix Fabric MCP Server        │
│   (TypeScript/Node.js)             │
│                                    │
│  ┌────────────────────────────┐  │
│  │  MCP Server Core       │  │
│  │  - Tool Definitions    │  │
│  │  - Request Handlers    │  │
│  │  - Stdio Transport     │  │
│  └──────────┬─────────────┘  │
│             │                    │
│  ┌──────────┴─────────────┐  │
│  │   API Client (Axios)   │  │
│  │   - Auth Headers       │  │
│  │   - Error Handling     │  │
│  └──────────┬─────────────┘  │
└─────────────┴────────────────────┘
             │ HTTPS/REST
             │ Bearer Token Auth
             │
┌────────────┴───────────────────┐
│   Equinix Fabric API         │
│   (api.equinix.com)          │
│                               │
│   • Ports                    │
│   • Connections              │
│   • Cloud Routers           │
│   • Service Profiles        │
│   • Service Tokens          │
└───────────────────────────────┘
```

## Component Details

### 1. MCP Server Core

**Location**: `src/index.ts`

**Responsibilities**:
- Initialize MCP server with capabilities
- Define tool schemas
- Handle tool invocation requests
- Manage stdio transport
- Format responses for Claude

**Key Classes**:
- `Server`: Main MCP server instance
- `StdioServerTransport`: Communication channel with Claude

### 2. API Client

**Implementation**: Axios HTTP client

**Configuration**:
- Base URL: `https://api.equinix.com`
- Authentication: Bearer token from environment
- Content-Type: `application/json`

**Features**:
- Automatic auth header injection
- Error response handling
- Request/response logging

### 3. Tool Handlers

Each tool follows this pattern:

```typescript
case 'tool_name': {
  // 1. Extract and validate parameters
  const { param1, param2 } = args as any;
  
  // 2. Make API request
  const response = await apiClient.get('/fabric/v4/endpoint');
  
  // 3. Format and return response
  return {
    content: [{
      type: 'text',
      text: JSON.stringify(response.data, null, 2)
    }]
  };
}
```

## Data Flow

### 1. User Request Flow

```
User Input (Natural Language)
       ↓
Claude processes and identifies needed tool
       ↓
Claude sends tool invocation via MCP
       ↓
MCP Server receives tool request
       ↓
Server validates parameters
       ↓
Server calls Equinix API
       ↓
API returns data
       ↓
Server formats response
       ↓
Claude receives structured data
       ↓
Claude presents to user in natural language
```

### 2. Connection Creation Flow

```
User: "Create connection from Singapore to AWS"
       ↓
Claude asks for details (bandwidth, port, etc.)
       ↓
User provides information
       ↓
Claude calls create_fabric_connection tool
       ↓
MCP Server validates configuration
       ↓
MCP Server POSTs to /fabric/v4/connections
       ↓
Equinix API creates connection
       ↓
API returns connection UUID and details
       ↓
Claude confirms success to user
```

## Tool Categories

### Read Operations (GET)
- `list_fabric_ports`
- `get_fabric_port`
- `list_fabric_connections`
- `get_fabric_connection`
- `get_connection_stats`
- `list_fabric_routers`
- `get_fabric_router`
- `list_service_profiles`
- `get_service_profile`
- `list_service_tokens`
- `get_service_token`
- `list_metros`
- `search_connections`

### Write Operations (POST/PATCH/DELETE)
- `create_fabric_connection`
- `update_connection`
- `delete_connection`
- `create_fabric_router`
- `update_fabric_router`
- `delete_fabric_router`
- `create_service_token`
- `delete_service_token`

### Validation Operations
- `validate_connection_config`

## Security Architecture

### Authentication Flow

```
1. User generates API token in Equinix Portal
2. User stores token in Claude Desktop config
3. MCP Server reads token from environment
4. MCP Server adds token to API requests
5. Equinix API validates token
6. API returns data or error
```

### Security Layers

1. **Local Storage**: Token stored in local config file
2. **Environment Variable**: Token passed via env vars
3. **HTTPS**: All API calls over TLS
4. **Bearer Auth**: Token in Authorization header
5. **No Persistence**: Server doesn't store credentials

## Error Handling

### Error Flow

```
API Error Occurs
       ↓
Axios catches error
       ↓
MCP Server extracts error details
       ↓
Server formats error message
       ↓
Server returns with isError: true
       ↓
Claude presents error to user
       ↓
Claude suggests remediation
```

### Error Types Handled

- **401 Unauthorized**: Invalid/expired token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Server Error**: Equinix API issues
- **Network Errors**: Connection failures

## Configuration Management

### Configuration Sources

1. **Environment Variables**
   - `EQUINIX_API_TOKEN`: Required API token

2. **Claude Desktop Config**
   - Server command and args
   - Environment variable injection
   - Multiple server instances

3. **Package.json**
   - Dependencies
   - Scripts
   - Metadata

## Build & Deploy Process

### Development Flow

```
Edit TypeScript source
       ↓
npm run watch (auto-compile)
       ↓
Test with Claude Desktop
       ↓
Iterate
```

### Build Process

```
npm run build
       ↓
TypeScript compiler (tsc)
       ↓
Generate dist/ directory
       ↓
Compile .ts to .js
       ↓
Generate .d.ts declarations
       ↓
Ready for distribution
```

### Distribution

```
npm publish
       ↓
Publish to npm registry
       ↓
Users install via npm
       ↓
Users run via npx
```

## Performance Considerations

### Response Times

- **List operations**: 500ms - 2s
- **Get operations**: 300ms - 1s
- **Create operations**: 2s - 10s
- **Update operations**: 1s - 5s
- **Delete operations**: 1s - 3s

### Optimization Strategies

1. **Pagination**: Limit results to reduce payload
2. **Filtering**: Use API filters to reduce data
3. **Caching**: Client-side (Claude) caches responses
4. **Parallel Requests**: Future enhancement

## Scalability

### Current Limitations

- Single user per instance
- Synchronous request handling
- No request queuing
- No connection pooling

### Future Enhancements

- Request batching
- Response caching
- Concurrent request handling
- Connection pooling

## Monitoring & Observability

### Logging

**Current**:
- Server startup messages to stderr
- Error messages to stderr
- API errors in tool responses

**Future**:
- Structured logging
- Request/response logging
- Performance metrics
- Error tracking

### Debugging

1. **Claude Desktop Logs**: Check application logs
2. **Network Inspection**: Use API debugging tools
3. **Source Maps**: TypeScript debug support
4. **Console Logging**: Add debug statements

## Dependencies

### Core Dependencies

- `@modelcontextprotocol/sdk`: ^0.5.0 - MCP protocol implementation
- `axios`: ^1.6.0 - HTTP client
- `zod`: ^3.22.0 - Schema validation

### Dev Dependencies

- `typescript`: ^5.3.0 - TypeScript compiler
- `@types/node`: ^20.0.0 - Node.js type definitions
- `ts-node`: ^10.9.0 - TypeScript execution

## Testing Strategy

### Current Testing

- Manual testing with Claude Desktop
- Real API integration testing
- TypeScript compilation checks

### Future Testing

- Unit tests for tool handlers
- Integration tests with mock API
- End-to-end tests
- Performance benchmarks

## Extensibility

### Adding New Tools

1. Define tool schema in `tools` array
2. Add handler in `CallToolRequestSchema`
3. Implement API call logic
4. Format response
5. Update documentation
6. Test thoroughly

### Adding New Features

1. Check Equinix API documentation
2. Design tool interface
3. Implement handler
4. Add error handling
5. Document usage
6. Submit PR

## API Versioning

### Current Version

- Equinix Fabric API: v4
- MCP Server: 1.0.0
- MCP SDK: 0.5.0

### Version Strategy

- Semantic versioning (semver)
- Breaking changes = major version
- New features = minor version
- Bug fixes = patch version

## Deployment Scenarios

### Local Development

```bash
git clone repo
npm install
npm run build
Configure Claude Desktop
Test locally
```

### Global Installation

```bash
npm install -g equinix-fabric-mcp
Configure Claude Desktop with npx
Use immediately
```

### Multiple Environments

```json
{
  "mcpServers": {
    "equinix-prod": { ... },
    "equinix-staging": { ... },
    "equinix-dev": { ... }
  }
}
```

## Best Practices

### Code Style

- Use TypeScript strict mode
- Follow existing patterns
- Add type annotations
- Document complex logic
- Keep functions focused

### Error Handling

- Always catch API errors
- Provide helpful error messages
- Include error context
- Return structured errors

### Security

- Never log tokens
- Validate all inputs
- Use HTTPS only
- Rotate credentials
- Follow least privilege

## Future Architecture Plans

### Planned Enhancements

1. **Caching Layer**: Reduce API calls
2. **Request Queue**: Handle concurrent requests
3. **Batch Operations**: Multiple resources at once
4. **Webhook Support**: Real-time updates
5. **Enhanced Validation**: Pre-flight checks
6. **Monitoring**: Performance metrics
7. **Testing**: Automated test suite

### Long-term Vision

- Multi-protocol support (WebSocket)
- Real-time monitoring integration
- Advanced analytics
- Template library
- Cost optimization AI
- Automated healing
