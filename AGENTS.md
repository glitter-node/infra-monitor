Project: InfraMonitor

Backend
FastAPI
Uvicorn

Python
3.12

Architecture
Service oriented structure.

Use async endpoints.
Business logic must not exist in API routers.
All logic must exist in services.

Coding rules
- Python 3.12
- Use type hints
- Use async endpoints
- Use services layer
- Return JSON responses
- No blocking shell commands in API layer
- Use psutil for system metrics
- Use socket for port checks

Directory rules
app/api
app/services
app/models
app/static
app/templates

API design

The project must implement these four APIs first.

GET /api/system

Purpose
Return system metrics.

Fields
hostname
uptime_seconds
load_average
memory_total
memory_used
memory_percent
disk_total
disk_used
disk_percent

Example response

{
  "hostname": "infra-node",
  "uptime_seconds": 102394,
  "load_average": [0.12, 0.08, 0.05],
  "memory_total": 16777216,
  "memory_used": 8123456,
  "memory_percent": 48.4,
  "disk_total": 512000000000,
  "disk_used": 132000000000,
  "disk_percent": 25.7
}


GET /api/ports

Purpose
Check important service ports.

Default ports

80
443
25
53
8000
3306
6379

Response format

{
  "80": "open",
  "443": "open",
  "3306": "closed"
}


GET /api/upstreams

Purpose
Check internal application upstream services.

Default targets

127.0.0.1:8000
127.0.0.1:8100

Response

{
  "127.0.0.1:8000": "running",
  "127.0.0.1:8100": "down"
}


GET /api/status

Purpose
Unified infrastructure status endpoint.

This API aggregates

system
ports
upstreams

Example response

{
  "system": {...},
  "ports": {...},
  "upstreams": {...}
}


Service layer design

system_service.py
collect_system_metrics()

port_service.py
check_ports()

upstream_service.py
check_upstreams()

status_service.py
aggregate_status()

API routers must only call services.
