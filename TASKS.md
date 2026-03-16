Project: InfraMonitor

Purpose

Implement a small infrastructure monitoring service using FastAPI.

The service must expose infrastructure and service health status
so that a single endpoint (monitor.glitter.kr) can be used to observe
system and public service availability.


Task execution rules

- Complete tasks in order
- Do not skip tasks
- Do not introduce new frameworks
- Follow project directory structure


Project structure

app/
  main.py
  api/
  services/
  models/
  static/
  templates/


Task 1

Create service modules.

Files

app/services/system_service.py
app/services/port_service.py
app/services/upstream_service.py
app/services/http_service.py
app/services/status_service.py


Task 2

Implement system metrics collection.

File

app/services/system_service.py

Function

collect_system_metrics()

Requirements

- Use psutil
- Return hostname
- Return uptime_seconds
- Return load_average
- Return memory_total
- Return memory_used
- Return memory_percent
- Return disk_total
- Return disk_used
- Return disk_percent


Task 3

Implement port monitoring.

File

app/services/port_service.py

Function

check_ports()

Default ports

22
80
443
25
53
3306
6379

Requirements

- Use python socket
- Attempt TCP connection
- Return open or closed


Task 4

Implement upstream service monitoring.

File

app/services/upstream_service.py

Function

check_upstreams()

Default upstream targets

127.0.0.1:8009

Requirements

- Test TCP connection
- Return running or down


Task 5

Implement public HTTP service monitoring.

File

app/services/http_service.py

Function

check_http_services()

Default targets

https://glitter.im
https://policy.glitter.kr
https://obs.glitter.kr

Requirements

- Perform HTTP GET request
- Timeout 3 seconds
- Return status code
- Return ok if status < 500
- Return down if connection fails


Task 6

Implement status aggregation.

File

app/services/status_service.py

Function

aggregate_status()

Requirements

Combine results from

system_service
port_service
upstream_service
http_service

Return

{
  "system": {},
  "ports": {},
  "upstreams": {},
  "services": {}
}


Task 7

Create API router.

File

app/api/monitor.py

Endpoints

GET /api/system
GET /api/ports
GET /api/upstreams
GET /api/services
GET /api/status

Rules

API routers must call services only.


Task 8

Register router in FastAPI app.

File

app/main.py

Requirements

Create FastAPI app.
Include router from app/api.


Task 9

Run server.

Command

uvicorn app.main:app --host 127.0.0.1 --port 9510


Expected API behavior


/api/system
returns system metrics


/api/ports
returns port status


/api/upstreams
returns upstream service status


/api/services
returns public HTTP service status


/api/status
returns combined infrastructure status