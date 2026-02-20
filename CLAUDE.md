# CLAUDE.md — equinix-fabric-mcp

MCP server for the Equinix Fabric API (connections, ports, routers, service profiles, metros).

## Canonical files

| File | Role |
|------|------|
| `server_v2.py` | **Active MCP server** (v2.1) — use this |
| `http_wrapper.py` | HTTP/REST wrapper for Postman testing only |
| `bridge_server.py` | stdio bridge |
| `list_ports.py` | Standalone utility — list ports without MCP |
| `server.py`, `server2.py` | Old versions — do not use |
| `server_v2.py.bak`, `server_v2_*.py.bak` | Snapshots — do not edit |

When making changes, always edit `server_v2.py`. Leave .bak files untouched.

## Auth

OAuth2 client_credentials flow. Token URL: `https://api.equinix.com/oauth2/v1/token`

```bash
cp env.example .env
# Add EQUINIX_CLIENT_ID and EQUINIX_CLIENT_SECRET
```

Credentials must be in `.env` (Docker) or exported in the shell (direct run). Never hardcode — `claude_config_snippet.json` in this repo has an outdated credential example, ignore it.

## Running

### As an MCP server (stdio — for Claude/Cursor integration)

```bash
source venv/bin/activate
python server_v2.py
```

### As an HTTP server (for Postman testing)

```bash
# Docker network must exist first
docker network create equinix-network 2>/dev/null || true

# Start the HTTP wrapper on :8000
docker-compose up -d

# Health check
curl http://localhost:8000/health

# Stop
docker-compose down
```

Swagger docs available at `http://localhost:8000/docs` when running.

## Testing

```bash
# Full test cycle (start Docker, health check, Newman tests)
./run_tests.sh start       # start + health checks
./run_tests.sh test        # start + Newman Postman tests
./run_tests.sh scenarios   # start + curl scenario tests
./run_tests.sh status      # show Docker status + logs
./run_tests.sh stop        # stop containers
```

Manual curl tests:
```bash
curl http://localhost:8000/api/metros
curl http://localhost:8000/api/service-profiles?limit=5
curl http://localhost:8000/tools
```

## Key endpoints (HTTP wrapper)

- `GET /health` — health check
- `GET /tools` — list all MCP tools
- `GET /api/ports` — list ports
- `GET /api/connections` — list connections
- `POST /api/connections/search` — filter connections (e.g. `{"filter": {"state": "ACTIVE"}}`)
- `GET /api/metros` — list metros
- `GET /api/service-profiles` — list service profiles
- `POST /api/tool` — execute any MCP tool by name

## MCP tools exposed

Ports, connections (CRUD + search + validate + stats), routers (CRUD), metros, service profiles, service tokens.

## Docker

Network: `equinix-network` (external — must be created before `docker-compose up`)
Port: `8000:8000`
Logs: `./logs/`

## Venv

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Dependencies

`mcp`, `httpx`, `fastapi`, `uvicorn`, `pydantic`
