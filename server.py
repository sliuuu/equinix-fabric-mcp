"""
Equinix Fabric MCP Server v2.2
A Model Context Protocol server for querying and managing Equinix Fabric infrastructure
"""

import os
import json
import asyncio
from typing import Any, Optional, Dict, List
from datetime import datetime
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

# Initialize the MCP server
app = Server("equinix-fabric")

# API Configuration
API_BASE_URL = "https://api.equinix.com"
OAUTH_URL = f"{API_BASE_URL}/oauth2/v1/token"

class EquinixClient:
    """Client for Equinix Fabric API"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token: Optional[str] = None
        self.token_expiry: float = 0
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def get_access_token(self) -> str:
        """Get OAuth2 access token with caching"""
        import time
        
        # Return cached token if still valid
        if self.access_token and time.time() < self.token_expiry:
            return self.access_token
            
        response = await self.http_client.post(
            OAUTH_URL,
            json={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            },
            headers={"content-type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        self.access_token = data["access_token"]
        # Set expiry to 1 minute before actual expiration
        self.token_expiry = time.time() + data.get("expires_in", 3600) - 60
        return self.access_token
    
    async def make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make authenticated API request"""
        token = await self.get_access_token()
        headers = {
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
        }
        
        url = f"{API_BASE_URL}{endpoint}"
        response = await self.http_client.request(
            method, url, headers=headers, **kwargs
        )
        response.raise_for_status()
        return response.json()
    
    # ========== READ OPERATIONS (Existing) ==========
    
    async def list_ports(self, offset: int = 0, limit: int = 20) -> dict:
        """List all Fabric ports"""
        return await self.make_request(
            "GET", 
            f"/fabric/v4/ports?offset={offset}&limit={limit}"
        )
    
    async def get_port(self, port_id: str) -> dict:
        """Get details of a specific port"""
        return await self.make_request("GET", f"/fabric/v4/ports/{port_id}")
    
    async def list_connections(self, offset: int = 0, limit: int = 20) -> dict:
        """List Fabric connections via search endpoint with pagination"""
        search_body = {
            "filter": {},
            "pagination": {"offset": offset, "limit": limit}
        }
        return await self.make_request(
            "POST",
            "/fabric/v4/connections/search",
            json=search_body
        )
    
    async def get_connection(self, connection_id: str) -> dict:
        """Get details of a specific connection"""
        return await self.make_request(
            "GET", 
            f"/fabric/v4/connections/{connection_id}"
        )
    
    async def get_connection_stats(
        self,
        connection_id: str,
        from_ts: Optional[str] = None,
        to_ts: Optional[str] = None,
        interval: Optional[str] = None,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,
        timeGranularity: Optional[str] = None,
    ) -> dict:
        """Not supported: Fabric v4 does not expose /connections/{uuid}/stats.

        Use get_connection(connection_id) for state/metadata or the connections search
        endpoints for filtered listings. Refer to Equinix Fabric v4 docs.
        """
        raise NotImplementedError(
            "Connection stats endpoint is not available in Fabric v4. "
            "Use GET /fabric/v4/connections/{uuid} or search endpoints instead."
        )
    
    async def list_routers(self, offset: int = 0, limit: int = 20) -> dict:
        """List Cloud Routers using search endpoint"""
        search_body = {
            "filter": {},
            "pagination": {"offset": offset, "limit": limit}
        }
        return await self.make_request(
            "POST",
            "/fabric/v4/routers/search",
            json=search_body
        )
    
    async def get_router(self, router_id: str) -> dict:
        """Get Cloud Router details using search endpoint"""
        search_body = {
            "filter": {
                "property": "/uuid",
                "operator": "=",
                "values": [router_id]
            },
            "pagination": {"offset": 0, "limit": 1}
        }
        result = await self.make_request(
            "POST",
            "/fabric/v4/routers/search",
            json=search_body
        )
        # Return the first (and only) result if found
        if result.get("data") and len(result["data"]) > 0:
            return result["data"][0]
        else:
            raise ValueError(f"Cloud Router with ID {router_id} not found")
    
    async def search_connections(self, query: dict) -> dict:
        """Search connections with filters"""
        return await self.make_request(
            "POST",
            "/fabric/v4/connections/search",
            json=query
        )
    
    async def search_routers(self, query: dict) -> dict:
        """Search Cloud Routers with filters"""
        return await self.make_request(
            "POST",
            "/fabric/v4/routers/search",
            json=query
        )
    
    async def list_metros(self) -> dict:
        """List available metros"""
        return await self.make_request("GET", "/fabric/v4/metros")
    
    # ========== WRITE OPERATIONS (Existing) ==========
    
    async def create_connection(self, connection_data: dict) -> dict:
        """Create a new Fabric connection"""
        payload = self._build_connection_payload(connection_data)
        return await self.make_request(
            "POST",
            "/fabric/v4/connections",
            json=payload
        )
    
    async def update_connection(self, connection_id: str, update_data: dict) -> dict:
        """Update an existing connection"""
        payload = []
        
        if "name" in update_data:
            payload.append({
                "op": "replace",
                "path": "/name",
                "value": update_data["name"]
            })
        
        if "description" in update_data:
            payload.append({
                "op": "replace",
                "path": "/description",
                "value": update_data["description"]
            })
        
        if "bandwidth" in update_data:
            payload.append({
                "op": "replace",
                "path": "/bandwidth",
                "value": update_data["bandwidth"]
            })
        
        if "notifications" in update_data:
            payload.append({
                "op": "replace",
                "path": "/notifications",
                "value": [{"type": "ALL", "emails": update_data["notifications"]}]
            })
        
        return await self.make_request(
            "PATCH",
            f"/fabric/v4/connections/{connection_id}",
            json=payload
        )
    
    async def delete_connection(self, connection_id: str) -> dict:
        """Delete a connection"""
        return await self.make_request(
            "DELETE",
            f"/fabric/v4/connections/{connection_id}"
        )
    
    async def validate_connection(self, connection_data: dict) -> dict:
        """Validate connection configuration without creating it"""
        payload = self._build_connection_payload(connection_data)
        return await self.make_request(
            "POST",
            "/fabric/v4/connections/validate",
            json=payload
        )
    
    # ========== CLOUD ROUTER MANAGEMENT (New) ==========
    
    async def create_router(self, router_data: dict) -> dict:
        """Not supported: Cloud Routers not available in Fabric v4 API"""
        raise NotImplementedError(
            "Cloud Routers are not available in Fabric v4 API. "
            "Use Fabric connections and service profiles instead."
        )
    
    async def update_router(self, router_id: str, update_data: dict) -> dict:
        """Not supported: Cloud Routers not available in Fabric v4 API"""
        raise NotImplementedError(
            "Cloud Routers are not available in Fabric v4 API. "
            "Use Fabric connections and service profiles instead."
        )
    
    async def delete_router(self, router_id: str) -> dict:
        """Not supported: Cloud Routers not available in Fabric v4 API"""
        raise NotImplementedError(
            "Cloud Routers are not available in Fabric v4 API. "
            "Use Fabric connections and service profiles instead."
        )
    
    # ========== SERVICE PROFILES ==========
    
    async def list_service_profiles(
        self, 
        offset: int = 0, 
        limit: int = 20,
        metro_code: Optional[str] = None,
        service_type: Optional[str] = None,
        name: Optional[str] = None
    ) -> dict:
        """List available service profiles"""
        params = f"offset={offset}&limit={limit}"
        
        if metro_code:
            params += f"&filter[metroCode]={metro_code}"
        if service_type:
            params += f"&filter[type]={service_type}"
        if name:
            params += f"&filter[name]={name}"
        
        return await self.make_request(
            "GET",
            f"/fabric/v4/serviceProfiles?{params}"
        )
    
    async def get_service_profile(self, profile_uuid: str) -> dict:
        """Get details of a specific service profile"""
        return await self.make_request(
            "GET",
            f"/fabric/v4/serviceProfiles/{profile_uuid}"
        )
    
    # ========== SERVICE TOKENS ==========
    
    async def create_service_token(self, token_data: dict) -> dict:
        """Create a service token"""
        payload = {
            "type": token_data["type"],
            "name": token_data["name"],
            "expirationDateTime": token_data["expiration_date"]
        }
        
        if "description" in token_data:
            payload["description"] = token_data["description"]
        
        if "notifications" in token_data:
            payload["notifications"] = [
                {"type": "ALL", "emails": token_data["notifications"]}
            ]
        
        if "service_token_connection" in token_data:
            stc = token_data["service_token_connection"]
            payload["serviceTokenConnection"] = {
                "type": stc["type"]
            }
            
            if "supported_bandwidths" in stc:
                payload["serviceTokenConnection"]["supportedBandwidths"] = stc["supported_bandwidths"]
            
            if "a_side" in stc:
                payload["serviceTokenConnection"]["aSide"] = {
                    "accessPoint": self._build_access_point(stc["a_side"])
                }
        
        return await self.make_request(
            "POST",
            "/fabric/v4/serviceTokens",
            json=payload
        )
    
    async def list_service_tokens(self, offset: int = 0, limit: int = 20) -> dict:
        """List service tokens"""
        return await self.make_request(
            "GET",
            f"/fabric/v4/serviceTokens?offset={offset}&limit={limit}"
        )
    
    async def get_service_token(self, token_uuid: str) -> dict:
        """Get details of a specific service token"""
        return await self.make_request(
            "GET",
            f"/fabric/v4/serviceTokens/{token_uuid}"
        )
    
    async def delete_service_token(self, token_uuid: str) -> dict:
        """Delete a service token"""
        return await self.make_request(
            "DELETE",
            f"/fabric/v4/serviceTokens/{token_uuid}"
        )
    
    # ========== HELPER METHODS ==========
    
    def _build_connection_payload(self, data: dict) -> dict:
        """Build connection payload from input data"""
        payload = {
            "type": data["type"],
            "name": data["name"],
            "bandwidth": data["bandwidth"],
            "aSide": {
                "accessPoint": self._build_access_point(data["a_side"])
            },
            "zSide": {
                "accessPoint": self._build_access_point(data["z_side"])
            }
        }
        
        if "description" in data:
            payload["description"] = data["description"]
        
        if "notifications" in data:
            payload["notifications"] = [
                {"type": "ALL", "emails": data["notifications"]}
            ]
        
        if "redundancy" in data:
            payload["redundancy"] = data["redundancy"]
        
        if "project_id" in data:
            payload["project"] = {"projectId": data["project_id"]}
        
        return payload
    
    def _build_access_point(self, side: dict) -> dict:
        """Build access point configuration"""
        access_point = {}
        
        if side["type"] == "port":
            access_point["type"] = "COLO"
            access_point["port"] = {"uuid": side["port_uuid"]}
            
            if "vlan" in side:
                access_point["linkProtocol"] = {
                    "type": "DOT1Q",
                    "vlanTag": side["vlan"]
                }
            else:
                access_point["linkProtocol"] = {"type": "UNTAGGED"}
        
        elif side["type"] == "virtual_device":
            access_point["type"] = "VD"
            access_point["virtualDevice"] = {"uuid": side["virtual_device_uuid"]}
            
            if "vlan" in side:
                access_point["interface"] = {
                    "type": "NETWORK",
                    "vlanTag": side["vlan"]
                }
        
        elif side["type"] == "service_token":
            access_point["type"] = "SERVICE_TOKEN"
            access_point["serviceToken"] = {"uuid": side["service_token_uuid"]}
        
        elif side["type"] == "service_profile":
            access_point["type"] = "SP"
            access_point["profile"] = {
                "uuid": side["service_profile_uuid"],
                "type": "L2_PROFILE"
            }
            if "seller_metro_code" in side:
                access_point["location"] = {"metroCode": side["seller_metro_code"]}
        
        return access_point

# Initialize the Equinix client
equinix_client: Optional[EquinixClient] = None

def init_client():
    """Initialize the Equinix client from environment variables"""
    global equinix_client
    client_id = os.getenv("EQUINIX_CLIENT_ID")
    client_secret = os.getenv("EQUINIX_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError(
            "EQUINIX_CLIENT_ID and EQUINIX_CLIENT_SECRET environment variables are required"
        )
    
    equinix_client = EquinixClient(client_id, client_secret)

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        # ========== READ OPERATIONS (Existing) ==========
        Tool(
            name="list_fabric_ports",
            description="List all Equinix Fabric ports in your account",
            inputSchema={
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "number",
                        "description": "Pagination offset (default: 0)",
                        "default": 0
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results to return (default: 20, max: 100)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_fabric_port",
            description="Get detailed information about a specific Fabric port",
            inputSchema={
                "type": "object",
                "properties": {
                    "port_id": {
                        "type": "string",
                        "description": "UUID of the port"
                    }
                },
                "required": ["port_id"]
            }
        ),
        Tool(
            name="list_fabric_connections",
            description="List all Fabric connections in your account",
            inputSchema={
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "number",
                        "description": "Pagination offset (default: 0)",
                        "default": 0
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results to return (default: 20, max: 100)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_fabric_connection",
            description="Get detailed information about a specific Fabric connection",
            inputSchema={
                "type": "object",
                "properties": {
                    "connection_id": {
                        "type": "string",
                        "description": "UUID of the connection"
                    }
                },
                "required": ["connection_id"]
            }
        ),
        Tool(
            name="get_connection_stats",
            description="Deprecated: Fabric v4 does not support connection stats endpoint",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_fabric_routers",
            description="List all Fabric Cloud Routers in your account",
            inputSchema={
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "number",
                        "description": "Pagination offset (default: 0)",
                        "default": 0
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results to return (default: 20, max: 100)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_fabric_router",
            description="Get detailed information about a specific Fabric Cloud Router",
            inputSchema={
                "type": "object",
                "properties": {
                    "router_id": {
                        "type": "string",
                        "description": "UUID of the router"
                    }
                },
                "required": ["router_id"]
            }
        ),
        Tool(
            name="search_connections",
            description="Search for connections using filters (name, state, bandwidth, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Filter by connection name (partial match)"
                    },
                    "state": {
                        "type": "string",
                        "description": "Filter by state (e.g., ACTIVE, PENDING, DEPROVISIONED)",
                        "enum": ["ACTIVE", "PENDING", "DEPROVISIONED", "PENDING_AUTO_APPROVAL"]
                    },
                    "offset": {
                        "type": "number",
                        "description": "Pagination offset (default: 0)",
                        "default": 0
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results (default: 20, max: 100)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="list_metros",
            description="List all available Equinix Fabric metro locations",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ========== CONNECTION MANAGEMENT (Existing) ==========
        Tool(
            name="create_fabric_connection",
            description="Creates a new Fabric virtual connection between two endpoints (ports, service profiles, or cloud providers). Returns the created connection with UUID and initial state.",
            inputSchema={
                "type": "object",
                "required": ["name", "type", "bandwidth", "a_side", "z_side"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Connection name (required)"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["EVPL_VC", "EPL_VC", "IPWAN_VC", "EPLAN_VC", "EVPLAN_VC"],
                        "description": "Connection type: EVPL_VC (Ethernet Virtual Private Line), EPL_VC (Ethernet Private Line), IPWAN_VC (IP VPN), EPLAN_VC (Ethernet Private LAN), EVPLAN_VC (Ethernet Virtual Private LAN)"
                    },
                    "bandwidth": {
                        "type": "number",
                        "description": "Bandwidth in Mbps (e.g., 50, 100, 500, 1000, 2000, 5000, 10000)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional connection description"
                    },
                    "notifications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Email addresses for connection notifications"
                    },
                    "a_side": {
                        "type": "object",
                        "required": ["type"],
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["port", "virtual_device", "service_token"],
                                "description": "A-side endpoint type"
                            },
                            "port_uuid": {
                                "type": "string",
                                "description": "Port UUID (required if type=port)"
                            },
                            "virtual_device_uuid": {
                                "type": "string",
                                "description": "Virtual device UUID (required if type=virtual_device)"
                            },
                            "service_token_uuid": {
                                "type": "string",
                                "description": "Service token UUID (required if type=service_token)"
                            },
                            "vlan": {
                                "type": "number",
                                "description": "VLAN tag (2-4094). Required for EVPL connections.",
                                "minimum": 2,
                                "maximum": 4094
                            }
                        }
                    },
                    "z_side": {
                        "type": "object",
                        "required": ["type"],
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["port", "virtual_device", "service_token", "service_profile"],
                                "description": "Z-side endpoint type"
                            },
                            "port_uuid": {
                                "type": "string",
                                "description": "Port UUID (required if type=port)"
                            },
                            "virtual_device_uuid": {
                                "type": "string",
                                "description": "Virtual device UUID (required if type=virtual_device)"
                            },
                            "service_token_uuid": {
                                "type": "string",
                                "description": "Service token UUID (required if type=service_token)"
                            },
                            "service_profile_uuid": {
                                "type": "string",
                                "description": "Service profile UUID (required if type=service_profile) - for connecting to cloud providers or partners"
                            },
                            "vlan": {
                                "type": "number",
                                "description": "VLAN tag (2-4094). Required for EVPL connections.",
                                "minimum": 2,
                                "maximum": 4094
                            },
                            "seller_metro_code": {
                                "type": "string",
                                "description": "Seller metro code (required for service_profile connections)"
                            }
                        }
                    },
                    "redundancy": {
                        "type": "object",
                        "properties": {
                            "priority": {
                                "type": "string",
                                "enum": ["PRIMARY", "SECONDARY"],
                                "description": "Redundancy priority for this connection"
                            },
                            "group": {
                                "type": "string",
                                "description": "Redundancy group identifier"
                            }
                        }
                    },
                    "project_id": {
                        "type": "string",
                        "description": "Project ID for the connection (enterprise feature)"
                    }
                }
            }
        ),
        Tool(
            name="update_connection",
            description="Updates an existing connection. Supports modifying name, description, bandwidth, and notifications.",
            inputSchema={
                "type": "object",
                "required": ["connection_uuid"],
                "properties": {
                    "connection_uuid": {
                        "type": "string",
                        "description": "UUID of the connection to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New connection name"
                    },
                    "description": {
                        "type": "string",
                        "description": "New connection description"
                    },
                    "bandwidth": {
                        "type": "number",
                        "description": "New bandwidth in Mbps (may incur charges)"
                    },
                    "notifications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Updated email addresses for notifications"
                    }
                }
            }
        ),
        Tool(
            name="delete_connection",
            description="Deletes a Fabric connection. This action cannot be undone and will terminate the connection.",
            inputSchema={
                "type": "object",
                "required": ["connection_uuid"],
                "properties": {
                    "connection_uuid": {
                        "type": "string",
                        "description": "UUID of the connection to delete"
                    }
                }
            }
        ),
        Tool(
            name="validate_connection_config",
            description="Validates a connection configuration before creation to check for errors, conflicts, or incompatibilities. Does not create the connection.",
            inputSchema={
                "type": "object",
                "required": ["connection_config"],
                "properties": {
                    "connection_config": {
                        "type": "object",
                        "description": "Connection configuration to validate (same structure as create_fabric_connection parameters)"
                    }
                }
            }
        ),
        
        # ========== CLOUD ROUTER MANAGEMENT (New) ==========
        Tool(
            name="create_fabric_router",
            description="Create a new Fabric Cloud Router in a specified metro location. Cloud Routers enable dynamic Layer 3 routing between multiple connections using BGP.",
            inputSchema={
                "type": "object",
                "required": ["name", "metro_code", "package"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Router name (e.g., 'FCR-SG0-MCP-CHULIU')"
                    },
                    "metro_code": {
                        "type": "string",
                        "description": "Metro code where router will be deployed (e.g., 'SG', 'NY', 'LD', 'SV', 'HK')"
                    },
                    "package": {
                        "type": "string",
                        "enum": ["STANDARD", "PRO", "ADVANCED"],
                        "description": "Router package type: STANDARD (basic routing, up to 10 connections), PRO (enhanced routing, more connections), ADVANCED (full BGP features, high capacity)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional router description"
                    },
                    "project_id": {
                        "type": "string",
                        "description": "Project ID to associate the router with (enterprise feature)"
                    },
                    "notifications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Email addresses for router notifications"
                    },
                    "order": {
                        "type": "object",
                        "properties": {
                            "purchaseOrderNumber": {
                                "type": "string",
                                "description": "Purchase order number for billing"
                            }
                        },
                        "description": "Optional order information"
                    }
                }
            }
        ),
        Tool(
            name="update_fabric_router",
            description="Update an existing Fabric Cloud Router. Supports modifying name, description, package, and notifications.",
            inputSchema={
                "type": "object",
                "required": ["router_uuid"],
                "properties": {
                    "router_uuid": {
                        "type": "string",
                        "description": "UUID of the router to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New router name"
                    },
                    "description": {
                        "type": "string",
                        "description": "New router description"
                    },
                    "package": {
                        "type": "string",
                        "enum": ["STANDARD", "PRO", "ADVANCED"],
                        "description": "New router package (may incur charges)"
                    },
                    "notifications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Updated email addresses for notifications"
                    }
                }
            }
        ),
        Tool(
            name="delete_fabric_router",
            description="Delete a Fabric Cloud Router. This action cannot be undone. All connections using this router must be deleted first.",
            inputSchema={
                "type": "object",
                "required": ["router_uuid"],
                "properties": {
                    "router_uuid": {
                        "type": "string",
                        "description": "UUID of the router to delete"
                    }
                }
            }
        ),
        
        # ========== SERVICE PROFILES (Existing) ==========
        Tool(
            name="list_service_profiles",
            description="Lists available service profiles that can be used as connection destinations. Service profiles represent cloud providers (AWS, Azure, GCP, Oracle, IBM) and network service providers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "metro_code": {
                        "type": "string",
                        "description": "Filter by metro code (e.g., 'SV', 'NY', 'LD')"
                    },
                    "service_type": {
                        "type": "string",
                        "enum": ["CLOUD_ROUTER", "EVPL", "EPL", "IPWAN"],
                        "description": "Filter by service type"
                    },
                    "name": {
                        "type": "string",
                        "description": "Filter by service profile name (partial match)"
                    },
                    "limit": {
                        "type": "number",
                        "default": 20,
                        "description": "Number of results to return (default: 20, max: 100)"
                    },
                    "offset": {
                        "type": "number",
                        "default": 0,
                        "description": "Pagination offset (default: 0)"
                    }
                }
            }
        ),
        Tool(
            name="get_service_profile",
            description="Gets detailed information about a specific service profile, including available metros, bandwidth options, and configuration requirements.",
            inputSchema={
                "type": "object",
                "required": ["profile_uuid"],
                "properties": {
                    "profile_uuid": {
                        "type": "string",
                        "description": "UUID of the service profile"
                    }
                }
            }
        ),
        
        # ========== SERVICE TOKENS (Existing) ==========
        Tool(
            name="create_service_token",
            description="Creates a service token that can be shared with another party to allow them to create a connection to your port or virtual device. Useful for enabling partner connections without sharing credentials.",
            inputSchema={
                "type": "object",
                "required": ["name", "type", "expiration_date"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Service token name"
                    },
                    "description": {
                        "type": "string",
                        "description": "Service token description"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["VC_TOKEN"],
                        "description": "Token type (currently only VC_TOKEN is supported)"
                    },
                    "expiration_date": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Token expiration date (ISO 8601 format, e.g., '2025-12-31T23:59:59Z')"
                    },
                    "service_token_connection": {
                        "type": "object",
                        "required": ["type"],
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["EVPL_VC"],
                                "description": "Connection type for the token"
                            },
                            "supported_bandwidths": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Allowed bandwidth values in Mbps (e.g., [50, 100, 500, 1000])"
                            },
                            "a_side": {
                                "type": "object",
                                "properties": {
                                    "port_uuid": {
                                        "type": "string",
                                        "description": "Port UUID to share"
                                    },
                                    "virtual_device_uuid": {
                                        "type": "string",
                                        "description": "Virtual device UUID to share"
                                    },
                                    "vlan": {
                                        "type": "number",
                                        "description": "VLAN tag (optional)"
                                    }
                                }
                            }
                        }
                    },
                    "notifications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Email addresses for token notifications"
                    }
                }
            }
        ),
        Tool(
            name="list_service_tokens",
            description="List all service tokens in your account",
            inputSchema={
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "number",
                        "description": "Pagination offset (default: 0)",
                        "default": 0
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of results to return (default: 20, max: 100)",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_service_token",
            description="Get details of a specific service token",
            inputSchema={
                "type": "object",
                "required": ["token_uuid"],
                "properties": {
                    "token_uuid": {
                        "type": "string",
                        "description": "UUID of the service token"
                    }
                }
            }
        ),
        Tool(
            name="delete_service_token",
            description="Delete a service token",
            inputSchema={
                "type": "object",
                "required": ["token_uuid"],
                "properties": {
                    "token_uuid": {
                        "type": "string",
                        "description": "UUID of the service token to delete"
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    if equinix_client is None:
        init_client()
    
    try:
        # ========== READ OPERATIONS (Existing) ==========
        if name == "list_fabric_ports":
            result = await equinix_client.list_ports(
                offset=arguments.get("offset", 0),
                limit=arguments.get("limit", 20)
            )
        elif name == "get_fabric_port":
            result = await equinix_client.get_port(arguments["port_id"])
        elif name == "list_fabric_connections":
            result = await equinix_client.list_connections(
                offset=arguments.get("offset", 0),
                limit=arguments.get("limit", 20)
            )
        elif name == "get_fabric_connection":
            result = await equinix_client.get_connection(arguments["connection_id"])
        elif name == "get_connection_stats":
            # Surface clear message since endpoint is not supported in Fabric v4
            raise NotImplementedError(
                "get_connection_stats is not supported: Fabric v4 does not provide "
                "/connections/{uuid}/stats. Use get_fabric_connection or search endpoints."
            )
        elif name == "list_fabric_routers":
            result = await equinix_client.list_routers(
                offset=arguments.get("offset", 0),
                limit=arguments.get("limit", 20)
            )
        elif name == "get_fabric_router":
            result = await equinix_client.get_router(arguments["router_id"])
        elif name == "search_connections":
            # Build search query
            filter_query = {"filter": {}, "pagination": {}}
            if "name" in arguments:
                filter_query["filter"]["name"] = arguments["name"]
            if "state" in arguments:
                filter_query["filter"]["state"] = arguments["state"]
            if "offset" in arguments:
                filter_query["pagination"]["offset"] = arguments.get("offset", 0)
            if "limit" in arguments:
                filter_query["pagination"]["limit"] = arguments.get("limit", 20)
            result = await equinix_client.search_connections(filter_query)
        elif name == "list_metros":
            result = await equinix_client.list_metros()
        
        # ========== CONNECTION MANAGEMENT (Existing) ==========
        elif name == "create_fabric_connection":
            result = await equinix_client.create_connection(arguments)
        elif name == "update_connection":
            connection_uuid = arguments.pop("connection_uuid")
            result = await equinix_client.update_connection(connection_uuid, arguments)
        elif name == "delete_connection":
            result = await equinix_client.delete_connection(arguments["connection_uuid"])
        elif name == "validate_connection_config":
            result = await equinix_client.validate_connection(arguments["connection_config"])
        
        # ========== CLOUD ROUTER MANAGEMENT (New) ==========
        elif name == "create_fabric_router":
            result = await equinix_client.create_router(arguments)
        elif name == "update_fabric_router":
            router_uuid = arguments.pop("router_uuid")
            result = await equinix_client.update_router(router_uuid, arguments)
        elif name == "delete_fabric_router":
            result = await equinix_client.delete_router(arguments["router_uuid"])
        
        # ========== SERVICE PROFILES (Existing) ==========
        elif name == "list_service_profiles":
            result = await equinix_client.list_service_profiles(
                offset=arguments.get("offset", 0),
                limit=arguments.get("limit", 20),
                metro_code=arguments.get("metro_code"),
                service_type=arguments.get("service_type"),
                name=arguments.get("name")
            )
        elif name == "get_service_profile":
            result = await equinix_client.get_service_profile(arguments["profile_uuid"])
        
        # ========== SERVICE TOKENS (Existing) ==========
        elif name == "create_service_token":
            result = await equinix_client.create_service_token(arguments)
        elif name == "list_service_tokens":
            result = await equinix_client.list_service_tokens(
                offset=arguments.get("offset", 0),
                limit=arguments.get("limit", 20)
            )
        elif name == "get_service_token":
            result = await equinix_client.get_service_token(arguments["token_uuid"])
        elif name == "delete_service_token":
            result = await equinix_client.delete_service_token(arguments["token_uuid"])
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP Error {e.response.status_code}: {e.response.text}"
        return [TextContent(type="text", text=f"Error calling {name}: {error_msg}")]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error calling {name}: {str(e)}"
        )]

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
