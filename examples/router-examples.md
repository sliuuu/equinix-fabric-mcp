# Cloud Router Configuration Examples

## Example 1: Basic Cloud Router (Standard Package)

```json
{
  "name": "FCR-SG-Basic",
  "metro_code": "SG",
  "package": "STANDARD",
  "description": "Basic cloud router for development environment",
  "notifications": ["devops@example.com"]
}
```

## Example 2: Production Cloud Router (PRO Package)

```json
{
  "name": "FCR-LD-Production",
  "metro_code": "LD",
  "package": "PRO",
  "description": "Production cloud router for London region",
  "notifications": [
    "network-ops@example.com",
    "cloud-team@example.com"
  ],
  "order": {
    "purchaseOrderNumber": "PO-2025-10001"
  }
}
```

## Example 3: Enterprise Cloud Router (Advanced Package)

```json
{
  "name": "FCR-SV-Enterprise",
  "metro_code": "SV",
  "package": "ADVANCED",
  "description": "High-capacity router for multi-cloud connectivity",
  "notifications": [
    "neteng@example.com",
    "cto@example.com"
  ],
  "order": {
    "purchaseOrderNumber": "PO-2025-10002"
  },
  "project_id": "project-abc123"
}
```

## Example 4: Regional Hub Router

```json
{
  "name": "FCR-HK-APAC-Hub",
  "metro_code": "HK",
  "package": "PRO",
  "description": "APAC regional hub router connecting multiple cloud providers",
  "notifications": ["apac-netops@example.com"]
}
```

## Example 5: Multi-Cloud Router Setup

### Router Creation
```json
{
  "name": "FCR-NY-MultiCloud",
  "metro_code": "NY",
  "package": "ADVANCED",
  "description": "Multi-cloud connectivity hub for AWS, Azure, and GCP",
  "notifications": ["multicloud-ops@example.com"]
}
```

### Connection to AWS
```json
{
  "name": "FCR-NY-to-AWS",
  "type": "EVPL_VC",
  "bandwidth": 1000,
  "a_side": {
    "type": "virtual_device",
    "virtual_device_uuid": "<router-uuid>"
  },
  "z_side": {
    "type": "service_profile",
    "service_profile_uuid": "<aws-dx-profile-uuid>",
    "seller_metro_code": "NY"
  }
}
```

### Connection to Azure
```json
{
  "name": "FCR-NY-to-Azure",
  "type": "EVPL_VC",
  "bandwidth": 500,
  "a_side": {
    "type": "virtual_device",
    "virtual_device_uuid": "<router-uuid>"
  },
  "z_side": {
    "type": "service_profile",
    "service_profile_uuid": "<azure-er-profile-uuid>",
    "seller_metro_code": "NY"
  }
}
```

### Connection to GCP
```json
{
  "name": "FCR-NY-to-GCP",
  "type": "EVPL_VC",
  "bandwidth": 500,
  "a_side": {
    "type": "virtual_device",
    "virtual_device_uuid": "<router-uuid>"
  },
  "z_side": {
    "type": "service_profile",
    "service_profile_uuid": "<gcp-interconnect-uuid>",
    "seller_metro_code": "NY"
  }
}
```

## Cloud Router Package Comparison

### STANDARD Package
- **Best for**: Development, testing, small deployments
- **Connections**: Up to 10
- **Throughput**: Basic
- **BGP Sessions**: Limited
- **Use Case**: Single cloud connection, dev/test environments

### PRO Package
- **Best for**: Production workloads, medium enterprises
- **Connections**: Up to 50
- **Throughput**: Enhanced
- **BGP Sessions**: Standard
- **Use Case**: Multi-cloud connectivity, production environments

### ADVANCED Package
- **Best for**: Large enterprises, high-capacity needs
- **Connections**: 100+
- **Throughput**: Maximum
- **BGP Sessions**: Advanced routing features
- **Use Case**: Complex multi-cloud architectures, hub-and-spoke designs

## Common Metro Codes for Routers

### Americas
- **NY**: New York
- **DC**: Washington DC
- **SV**: Silicon Valley
- **LA**: Los Angeles
- **CH**: Chicago
- **DA**: Dallas
- **SE**: Seattle
- **TO**: Toronto
- **SP**: São Paulo

### EMEA
- **LD**: London
- **AM**: Amsterdam
- **FR**: Frankfurt
- **PA**: Paris
- **MA**: Madrid
- **ST**: Stockholm
- **DU**: Dubai

### Asia-Pacific
- **SG**: Singapore
- **HK**: Hong Kong
- **TY**: Tokyo
- **OS**: Osaka
- **SY**: Sydney
- **ME**: Melbourne
- **SE**: Seoul

## Router Update Examples

### Upgrade Package
```json
{
  "router_uuid": "<router-uuid>",
  "package": "ADVANCED",
  "name": "FCR-SG-Production-Upgraded"
}
```

### Update Notifications
```json
{
  "router_uuid": "<router-uuid>",
  "notifications": [
    "network-team@example.com",
    "oncall@example.com"
  ]
}
```

## Best Practices

1. **Naming Convention**
   - Use prefix: FCR (Fabric Cloud Router)
   - Include metro code
   - Add environment or purpose
   - Example: `FCR-SG-Production-APAC`

2. **Package Selection**
   - Start with STANDARD for testing
   - Use PRO for production workloads
   - Choose ADVANCED for high-capacity or complex routing

3. **High Availability**
   - Deploy routers in multiple metros
   - Create redundant connections
   - Implement proper BGP configuration

4. **Monitoring**
   - Configure email notifications
   - Monitor connection health
   - Track bandwidth utilization
   - Set up alerts for issues

5. **Cost Optimization**
   - Right-size router packages
   - Monitor connection usage
   - Consolidate connections where possible
   - Review and optimize regularly

6. **Security**
   - Use BGP authentication
   - Implement proper AS filtering
   - Monitor for routing anomalies
   - Follow least-privilege principles

## Troubleshooting

### Router Not Showing Connections
- Verify router is in PROVISIONED state
- Check connection configurations
- Ensure connections reference correct router UUID

### Connection Failures
- Verify metro codes match
- Check bandwidth availability
- Ensure router package supports connection count
- Review BGP configuration

### Performance Issues
- Monitor router utilization
- Check for bandwidth constraints
- Consider upgrading router package
- Review connection distribution
