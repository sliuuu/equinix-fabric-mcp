"""
Equinix Fabric MCP Server v2.1
A Model Context Protocol server for querying and managing Equinix Fabric infrastructure
"""

import os
import json
import asyncio
from typing import Any, Optional
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
    
    # Additional methods would go here (truncated for brevity)
    # See full implementation in server.py

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
