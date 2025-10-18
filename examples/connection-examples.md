# Connection Configuration Examples

## Example 1: Port-to-Port Connection (EVPL)

```json
{
  "name": "SG-to-HK-Production",
  "type": "EVPL_VC",
  "bandwidth": 1000,
  "notifications": ["network-admin@example.com"],
  "a_side": {
    "type": "port",
    "port_uuid": "abc123-port-sg",
    "vlan": 100
  },
  "z_side": {
    "type": "port",
    "port_uuid": "def456-port-hk",
    "vlan": 200
  }
}
```

## Example 2: Connect to AWS Direct Connect

```json
{
  "name": "Production-AWS-Tokyo",
  "type": "EVPL_VC",
  "bandwidth": 500,
  "notifications": ["cloud-ops@example.com"],
  "a_side": {
    "type": "port",
    "port_uuid": "your-port-uuid",
    "vlan": 150
  },
  "z_side": {
    "type": "service_profile",
    "service_profile_uuid": "aws-dx-profile-uuid",
    "seller_metro_code": "TY"
  }
}
```

## Example 3: Connect to Azure ExpressRoute

```json
{
  "name": "Staging-Azure-Singapore",
  "type": "EVPL_VC",
  "bandwidth": 200,
  "notifications": ["azure-team@example.com"],
  "a_side": {
    "type": "port",
    "port_uuid": "your-port-uuid",
    "vlan": 300
  },
  "z_side": {
    "type": "service_profile",
    "service_profile_uuid": "azure-expressroute-uuid",
    "seller_metro_code": "SG"
  }
}
```

## Example 4: Connect to Google Cloud Interconnect

```json
{
  "name": "Analytics-GCP-London",
  "type": "EVPL_VC",
  "bandwidth": 1000,
  "notifications": ["gcp-admins@example.com"],
  "a_side": {
    "type": "port",
    "port_uuid": "your-port-uuid",
    "vlan": 400
  },
  "z_side": {
    "type": "service_profile",
    "service_profile_uuid": "gcp-interconnect-uuid",
    "seller_metro_code": "LD"
  }
}
```

## Example 5: Redundant Connection Pair

### Primary Connection
```json
{
  "name": "Production-Primary",
  "type": "EVPL_VC",
  "bandwidth": 1000,
  "notifications": ["netops@example.com"],
  "a_side": {
    "type": "port",
    "port_uuid": "port-a-uuid",
    "vlan": 100
  },
  "z_side": {
    "type": "port",
    "port_uuid": "port-z-uuid",
    "vlan": 200
  },
  "redundancy": {
    "priority": "PRIMARY",
    "group": "prod-redundancy-group-1"
  }
}
```

### Secondary Connection
```json
{
  "name": "Production-Secondary",
  "type": "EVPL_VC",
  "bandwidth": 1000,
  "notifications": ["netops@example.com"],
  "a_side": {
    "type": "port",
    "port_uuid": "port-a-backup-uuid",
    "vlan": 101
  },
  "z_side": {
    "type": "port",
    "port_uuid": "port-z-backup-uuid",
    "vlan": 201
  },
  "redundancy": {
    "priority": "SECONDARY",
    "group": "prod-redundancy-group-1"
  }
}
```

## Example 6: Using Service Token

```json
{
  "name": "Partner-Connection",
  "type": "EVPL_VC",
  "bandwidth": 100,
  "notifications": ["partner-ops@example.com"],
  "a_side": {
    "type": "service_token",
    "service_token_uuid": "token-uuid-from-partner"
  },
  "z_side": {
    "type": "port",
    "port_uuid": "your-port-uuid",
    "vlan": 500
  }
}
```

## Example 7: Cloud Router Connection

```json
{
  "name": "Multi-Cloud-Router-Connection",
  "type": "EVPL_VC",
  "bandwidth": 500,
  "a_side": {
    "type": "virtual_device",
    "virtual_device_uuid": "cloud-router-uuid"
  },
  "z_side": {
    "type": "service_profile",
    "service_profile_uuid": "aws-dx-profile-uuid",
    "seller_metro_code": "SV"
  }
}
```

## Common Metro Codes

- **SG**: Singapore
- **HK**: Hong Kong
- **TY**: Tokyo
- **SY**: Sydney
- **LD**: London
- **AM**: Amsterdam
- **FR**: Frankfurt
- **SV**: Silicon Valley
- **NY**: New York
- **DC**: Washington DC
- **CH**: Chicago
- **DA**: Dallas
- **LA**: Los Angeles
- **SE**: Seattle
- **TO**: Toronto
- **SP**: São Paulo

## Bandwidth Options

Common bandwidth values (in Mbps):
- 50
- 100
- 200
- 500
- 1000 (1 Gbps)
- 2000 (2 Gbps)
- 5000 (5 Gbps)
- 10000 (10 Gbps)

Check with Equinix for availability in your specific metro.

## Connection Types

- **EVPL_VC**: Ethernet Virtual Private Line (most common)
- **EPL_VC**: Ethernet Private Line
- **IPWAN_VC**: IP VPN
- **EPLAN_VC**: Ethernet Private LAN
- **EVPLAN_VC**: Ethernet Virtual Private LAN

## Best Practices

1. Use descriptive names that include environment, source, and destination
2. Always configure notifications for connection events
3. Use VLANs to segment traffic
4. Implement redundancy for production workloads
5. Monitor bandwidth usage regularly
6. Tag connections for better organization
7. Document connection purposes and owners
