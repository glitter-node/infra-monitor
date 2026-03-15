import asyncio
from typing import Any

from app.services.port_service import check_ports
from app.services.system_service import collect_system_metrics
from app.services.upstream_service import check_upstreams


async def aggregate_status() -> dict[str, Any]:
    system, ports, upstreams = await asyncio.gather(
        collect_system_metrics(),
        check_ports(),
        check_upstreams(),
    )

    return {
        "system": system,
        "ports": ports,
        "upstreams": upstreams,
    }
