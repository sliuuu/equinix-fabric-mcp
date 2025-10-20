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
