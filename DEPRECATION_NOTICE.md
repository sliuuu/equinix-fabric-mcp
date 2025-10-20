# Deprecation Notice - Version 2.2

## ⚠️ Deprecated Features

The following features have been deprecated in v2.2 due to Fabric v4 API limitations:

### 1. Connection Statistics (get_connection_stats)
**Deprecated**: October 20, 2025  
**Removed**: v2.2.0  
**Reason**: Endpoint not available in Fabric v4 API  

**Migration Path**:
```python
# Old (v2.1)
stats = get_connection_stats(\n    connection_id=\"abc-123\",\n    from_ts=\"2025-01-01\",\n    to_ts=\"2025-01-31\"\n)\n\n# New (v2.2)\nconnection = get_fabric_connection(\"abc-123\")\nprint(f\"State: {connection['state']}\")\nprint(f\"Bandwidth: {connection['bandwidth']}\")\n# For metrics, visit: https://fabric.equinix.com\n```

---

### 2. Cloud Router Create (create_fabric_router)
**Deprecated**: October 20, 2025  
**Removed**: v2.2.0  
**Reason**: Write endpoint not available in Fabric v4 API  

**Migration Path**:
- **Option A**: Use Fabric Portal GUI
- **Option B**: Use Terraform (see below)

**Terraform Example**:
```hcl
resource \"equinix_fabric_cloud_router\" \"my_router\" {\n  name         = \"FCR-SG-PROD\"\n  type         = \"XF_ROUTER\"\n  metro_code   = \"SG\"\n  package_code = \"PRO\"\n  \n  project {\n    project_id = var.project_id\n  }\n}\n```

---

### 3. Cloud Router Update (update_fabric_router)
**Deprecated**: October 20, 2025  
**Removed**: v2.2.0  
**Reason**: Write endpoint not available in Fabric v4 API  

**Migration Path**: Same as create_fabric_router

---

### 4. Cloud Router Delete (delete_fabric_router)
**Deprecated**: October 20, 2025  
**Removed**: v2.2.0  
**Reason**: Write endpoint not available in Fabric v4 API  

**Migration Path**: Use Fabric Portal or Terraform destroy

---

## 📅 Timeline

| Date | Action |\n|------|--------|\n| Oct 20, 2025 | v2.2.0 released with deprecations |\n| Oct 20, 2025 | Features return NotImplementedError |\n| Ongoing | Monitor Fabric API for future support |

---

## 🔄 Will These Features Return?

**Possibly**. If Equinix adds these endpoints to Fabric v4 or releases v5, we will:\n1. Restore functionality immediately\n2. Announce in changelog\n3. Update documentation\n4. Maintain backward compatibility

**Stay Updated**:
- Watch: https://developer.equinix.com/changelog
- Subscribe: https://github.com/sliuuu/equinix-fabric-mcp/releases

---

## ❓ Questions?

- Review the [Migration Guide](MIGRATION.md)
- Check [API Limitations](API_LIMITATIONS.md)
- Open an [Issue](https://github.com/sliuuu/equinix-fabric-mcp/issues)

---

**Document Version**: 1.0  
**For MCP Version**: 2.2.0  
**Last Updated**: October 20, 2025
