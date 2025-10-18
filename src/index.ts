#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import axios, { AxiosInstance } from 'axios';
import { z } from 'zod';

const API_BASE_URL = 'https://api.equinix.com';
const API_TOKEN = process.env.EQUINIX_API_TOKEN;

if (!API_TOKEN) {
  console.error('Error: EQUINIX_API_TOKEN environment variable is required');
  process.exit(1);
}

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json',
  },
});

const server = new Server(
  {
    name: 'equinix-fabric-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions
const tools = [
  {
    name: 'list_fabric_ports',
    description: 'List all Equinix Fabric ports in your account',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Number of results to return (default: 20, max: 100)',
          default: 20,
        },
        offset: {
          type: 'number',
          description: 'Pagination offset (default: 0)',
          default: 0,
        },
      },
    },
  },
  {
    name: 'get_fabric_port',
    description: 'Get detailed information about a specific Fabric port',
    inputSchema: {
      type: 'object',
      properties: {
        port_id: {
          type: 'string',
          description: 'UUID of the port',
        },
      },
      required: ['port_id'],
    },
  },
  {
    name: 'list_fabric_connections',
    description: 'List all Fabric connections in your account',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Number of results to return (default: 20, max: 100)',
          default: 20,
        },
        offset: {
          type: 'number',
          description: 'Pagination offset (default: 0)',
          default: 0,
        },
      },
    },
  },
  {
    name: 'get_fabric_connection',
    description: 'Get detailed information about a specific Fabric connection',
    inputSchema: {
      type: 'object',
      properties: {
        connection_id: {
          type: 'string',
          description: 'UUID of the connection',
        },
      },
      required: ['connection_id'],
    },
  },
  {
    name: 'create_fabric_connection',
    description: 'Create a new Fabric virtual connection between two endpoints',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Connection name' },
        type: {
          type: 'string',
          enum: ['EVPL_VC', 'EPL_VC', 'IPWAN_VC', 'EPLAN_VC', 'EVPLAN_VC'],
          description: 'Connection type',
        },
        bandwidth: { type: 'number', description: 'Bandwidth in Mbps' },
        a_side: {
          type: 'object',
          description: 'A-side endpoint configuration',
        },
        z_side: {
          type: 'object',
          description: 'Z-side endpoint configuration',
        },
      },
      required: ['name', 'type', 'bandwidth', 'a_side', 'z_side'],
    },
  },
  {
    name: 'list_fabric_routers',
    description: 'List all Fabric Cloud Routers in your account',
    inputSchema: {
      type: 'object',
      properties: {
        limit: { type: 'number', default: 20 },
        offset: { type: 'number', default: 0 },
      },
    },
  },
  {
    name: 'get_fabric_router',
    description: 'Get detailed information about a specific Fabric Cloud Router',
    inputSchema: {
      type: 'object',
      properties: {
        router_id: { type: 'string', description: 'UUID of the router' },
      },
      required: ['router_id'],
    },
  },
  {
    name: 'list_metros',
    description: 'List all available Equinix Fabric metro locations',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
];

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'list_fabric_ports': {
        const { limit = 20, offset = 0 } = args as any;
        const response = await apiClient.get('/fabric/v4/ports', {
          params: { limit, offset },
        });
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'get_fabric_port': {
        const { port_id } = args as any;
        const response = await apiClient.get(`/fabric/v4/ports/${port_id}`);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'list_fabric_connections': {
        const { limit = 20, offset = 0 } = args as any;
        const response = await apiClient.get('/fabric/v4/connections', {
          params: { limit, offset },
        });
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'get_fabric_connection': {
        const { connection_id } = args as any;
        const response = await apiClient.get(
          `/fabric/v4/connections/${connection_id}`
        );
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'create_fabric_connection': {
        const response = await apiClient.post('/fabric/v4/connections', args);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'list_fabric_routers': {
        const { limit = 20, offset = 0 } = args as any;
        const response = await apiClient.get('/fabric/v4/routers', {
          params: { limit, offset },
        });
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'get_fabric_router': {
        const { router_id } = args as any;
        const response = await apiClient.get(`/fabric/v4/routers/${router_id}`);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'list_metros': {
        const response = await apiClient.get('/fabric/v4/metros');
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}\n${error.response?.data ? JSON.stringify(error.response.data, null, 2) : ''}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Equinix Fabric MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
