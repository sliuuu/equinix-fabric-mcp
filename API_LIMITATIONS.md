# Equinix Fabric v4 API Limitations

This document explains known limitations in the Fabric v4 API that affect the MCP server.

## 🚫 Unavailable Endpoints

### 1. Connection Statistics
**Endpoint**: `GET /fabric/v4/connections/{uuid}/stats`

**Status**: Not available in Fabric v4

**Impact**: Cannot retrieve bandwidth usage, traffic statistics, or performance metrics via API

**Workaround**:
1. Use Fabric Portal for visual metrics
2. Use `get_fabric_connection()` for operational state
3. Implement external monitoring (Datadog, Prometheus, etc.)

**Example**:
```python
# ❌ This no longer works
stats = get_connection_stats(connection_id)

# ✅ Use this instead
connection = get_fabric_connection(connection_id)
print(f\"State: {connection['state']}\")
print(f\"Bandwidth: {connection['bandwidth']} Mbps\")
```

---

### 2. Cloud Router Write Operations
**Endpoints**:
- `POST /fabric/v4/cloudRouters` (create)
- `PATCH /fabric/v4/cloudRouters/{uuid}` (update)
- `DELETE /fabric/v4/cloudRouters/{uuid}` (delete)

**Status**: Not available in Fabric v4

**Impact**: Cannot create, modify, or delete Cloud Routers via API

**Workaround**:
1. **Fabric Portal**: https://fabric.equinix.com
2. **Terraform**: Use `equinix_fabric_cloud_router` resource
3. **API v5**: Wait for potential future API version

**Terraform Example**:
```hcl
resource \"equinix_fabric_cloud_router\" \"example\" {\n  name         = \"My-Router\"\n  type         = \"XF_ROUTER\"\n  metro_code   = \"SG\"\n  package_code = \"PRO\"\n}\n```

---

### 3. Cloud Router Direct GET
**Endpoint**: `GET /fabric/v4/cloudRouters/{uuid}`

**Status**: Not available in Fabric v4

**Impact**: Cannot directly retrieve router by UUID

**Workaround**: Use search endpoint with UUID filter

**Implementation**:
```python
# ✅ This works (using search)
router = get_fabric_router(router_uuid)
# Internally uses POST /fabric/v4/routers/search
```

---

## ✅ What Still Works

### Full Support
- ✅ Port management (list, get)
- ✅ Connection management (CRUD + search)
- ✅ Service profiles (list, get)
- ✅ Service tokens (CRUD)
- ✅ Metro locations (list)

### Read-Only Support
- ✅ Cloud Router list (via search)
- ✅ Cloud Router get (via search with UUID filter)

---

## 🔮 Future Possibilities

### Potential in v5 or v4 Updates
- Connection bandwidth statistics endpoint
- Cloud Router write operations
- Enhanced search capabilities
- GraphQL API alternative
- WebSocket support for real-time updates

### Community Requests
Track requests at: https://github.com/equinix/equinix-fabric-api/discussions

---

## 📞 Reporting API Issues

If you encounter other API limitations:

1. **Check Equinix API Docs**: https://developer.equinix.com/docs/fabric-v4
2. **Open GitHub Issue**: Include API endpoint and expected behavior
3. **Contact Equinix Support**: For official API roadmap questions

---

## 🔄 Monitoring API Changes

Stay updated on API changes:
- **Equinix API Changelog**: https://developer.equinix.com/changelog
- **MCP Server Releases**: https://github.com/sliuuu/equinix-fabric-mcp/releases
- **Community Discussions**: https://github.com/sliuuu/equinix-fabric-mcp/discussions

---

**Document Version**: 1.0  
**API Version**: Fabric v4  
**Last Updated**: October 20, 2025
