import asyncio
import time
from typing import Any

from app.config import REFRESH_INTERVAL
from app.services.dsm_service import check_dsm_services
from app.services.port_service import check_ports
from app.services.system_service import collect_system_metrics
from app.services.upstream_service import check_upstreams

_status_cache: dict[str, Any] = {
    "system": {},
    "ports": {},
    "upstreams": {},
    "services": {},
}
_last_refresh: float = 0.0
_refresh_lock = asyncio.Lock()
_refresh_task: asyncio.Task[None] | None = None


async def _collect_status_snapshot() -> dict[str, Any]:
    system, ports, upstreams, services = await asyncio.gather(
        collect_system_metrics(),
        check_ports(),
        check_upstreams(),
        check_dsm_services(),
    )
    return {
        "system": system,
        "ports": ports,
        "upstreams": upstreams,
        "services": services,
    }


async def _refresh_cache() -> None:
    global _status_cache, _last_refresh

    snapshot = await _collect_status_snapshot()
    async with _refresh_lock:
        _status_cache = snapshot
        _last_refresh = time.time()


def _cache_is_fresh() -> bool:
    return (time.time() - _last_refresh) < REFRESH_INTERVAL


async def refresh_status_cache() -> dict[str, Any]:
    async with _refresh_lock:
        if _cache_is_fresh() and _status_cache["system"]:
            return dict(_status_cache)

    await _refresh_cache()
    return dict(_status_cache)


def _schedule_background_refresh() -> None:
    global _refresh_task

    if _refresh_task is None or _refresh_task.done():
        _refresh_task = asyncio.create_task(_refresh_cache())


async def aggregate_status() -> dict[str, Any]:
    if not _status_cache["system"]:
        return await refresh_status_cache()

    if not _cache_is_fresh():
        _schedule_background_refresh()

    return dict(_status_cache)


async def get_system_status() -> dict[str, Any]:
    return dict((await aggregate_status())["system"])


async def get_ports_status() -> dict[str, str]:
    return dict((await aggregate_status())["ports"])


async def get_upstreams_status() -> dict[str, str]:
    return dict((await aggregate_status())["upstreams"])


async def get_services_status() -> dict[str, str]:
    return dict((await aggregate_status())["services"])
