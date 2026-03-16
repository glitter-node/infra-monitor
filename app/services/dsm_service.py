import asyncio
import re
import socket
from pathlib import Path

from app.config import DSM_PROXY_CONFIG_PATHS

_PROXY_PASS_PATTERN = re.compile(r"proxy_pass\s+http://(?:[\w\-.]+|\d{1,3}(?:\.\d{1,3}){3}):(\d+)")


def _discover_dsm_services_sync() -> list[dict[str, int]]:
    discovered_ports: set[int] = set()

    for config_path in DSM_PROXY_CONFIG_PATHS:
        directory = Path(config_path)
        if not directory.is_dir():
            continue

        for file_path in directory.rglob("*.conf"):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            for match in _PROXY_PASS_PATTERN.finditer(content):
                discovered_ports.add(int(match.group(1)))

    return [{"port": port} for port in sorted(discovered_ports)]


def _check_dsm_port(port: int) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", port))
        return "running" if result == 0 else "down"


async def discover_dsm_services() -> list[dict[str, int]]:
    return await asyncio.to_thread(_discover_dsm_services_sync)


async def check_dsm_services() -> dict[str, str]:
    services = await discover_dsm_services()
    ports = [service["port"] for service in services]
    service_results = await asyncio.gather(
        *(asyncio.to_thread(_check_dsm_port, port) for port in ports),
    )
    return {
        str(port): status
        for port, status in zip(ports, service_results, strict=True)
    }
