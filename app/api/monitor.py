from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.services.port_service import check_ports
from app.services.status_service import aggregate_status
from app.services.system_service import collect_system_metrics
from app.services.upstream_service import check_upstreams

router = APIRouter()


@router.get("/api/system")
async def get_system_metrics() -> dict[str, Any]:
    return await collect_system_metrics()


@router.get("/api/ports")
async def get_ports_status() -> dict[str, str]:
    return await check_ports()


@router.get("/api/upstreams")
async def get_upstreams_status() -> dict[str, str]:
    return await check_upstreams()


@router.get("/api/status")
async def get_status() -> dict[str, Any]:
    return await aggregate_status()


@router.get("/api/metrics", response_class=PlainTextResponse)
async def get_prometheus_metrics() -> PlainTextResponse:
    status = await aggregate_status()
    system = status["system"]
    ports = status["ports"]
    upstreams = status["upstreams"]

    lines = [
        f'infra_system_memory_percent {system["memory_percent"]}',
        f'infra_system_disk_percent {system["disk_percent"]}',
        "",
    ]

    for port, port_status in ports.items():
        if port_status == "open":
            lines.append(f'infra_port_open{{port="{port}"}} 1')
        else:
            lines.append(f'infra_port_closed{{port="{port}"}} 1')

    lines.append("")

    for target, upstream_status in upstreams.items():
        if upstream_status == "running":
            lines.append(f'infra_upstream_running{{target="{target}"}} 1')
        else:
            lines.append(f'infra_upstream_down{{target="{target}"}} 1')

    return PlainTextResponse("\n".join(lines), media_type="text/plain")
