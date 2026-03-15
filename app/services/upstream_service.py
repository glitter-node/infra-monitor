import socket

from app.config import UPSTREAM_TARGETS


async def check_upstreams() -> dict[str, str]:
    upstream_statuses: dict[str, str] = {}

    for target in UPSTREAM_TARGETS:
        host, port_text = target.rsplit(":", 1)
        port = int(port_text)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            upstream_statuses[target] = "running" if result == 0 else "down"

    return upstream_statuses
