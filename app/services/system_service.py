import asyncio
import os
import socket
import time
from typing import Any

import psutil


def _collect_system_metrics_sync() -> dict[str, Any]:
    virtual_memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")
    uptime_seconds = int(time.time() - psutil.boot_time())

    try:
        load_average_values = os.getloadavg()
        load_average = [
            float(load_average_values[0]),
            float(load_average_values[1]),
            float(load_average_values[2]),
        ]
    except (AttributeError, OSError):
        load_average = [0.0, 0.0, 0.0]

    return {
        "hostname": socket.gethostname(),
        "uptime_seconds": uptime_seconds,
        "load_average": load_average,
        "memory_total": virtual_memory.total,
        "memory_used": virtual_memory.used,
        "memory_percent": float(virtual_memory.percent),
        "disk_total": disk_usage.total,
        "disk_used": disk_usage.used,
        "disk_percent": float(disk_usage.percent),
    }


async def collect_system_metrics() -> dict[str, Any]:
    return await asyncio.to_thread(_collect_system_metrics_sync)
