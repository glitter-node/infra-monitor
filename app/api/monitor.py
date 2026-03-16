from typing import Any

from fastapi import APIRouter

from app.services.status_service import (
    aggregate_status,
    get_ports_status,
    get_services_status,
    get_system_status,
    get_upstreams_status,
)

router = APIRouter()


@router.get("/api/system")
async def read_system_metrics() -> dict[str, Any]:
    return await get_system_status()


@router.get("/api/ports")
async def read_ports_status() -> dict[str, str]:
    return await get_ports_status()


@router.get("/api/upstreams")
async def read_upstreams_status() -> dict[str, str]:
    return await get_upstreams_status()


@router.get("/api/services")
async def read_services_status() -> dict[str, str]:
    return await get_services_status()


@router.get("/api/status")
async def read_status() -> dict[str, Any]:
    return await aggregate_status()
