import asyncio
import socket

from app.config import UPSTREAM_TARGETS


def _check_single_upstream(host: str, port: int) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return "running" if result == 0 else "down"


async def check_upstreams() -> dict[str, str]:
    upstream_results = await asyncio.gather(
        *(
            asyncio.to_thread(_check_single_upstream, host, port)
            for host, port in UPSTREAM_TARGETS
        ),
    )
    return {
        f"{host}:{port}": status
        for (host, port), status in zip(UPSTREAM_TARGETS, upstream_results, strict=True)
    }
