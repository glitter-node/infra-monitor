import asyncio
import socket

from app.config import PORT_LIST


def _check_single_port(port: int) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", port))
        return "open" if result == 0 else "closed"


async def check_ports() -> dict[str, str]:
    port_results = await asyncio.gather(
        *(asyncio.to_thread(_check_single_port, port) for port in PORT_LIST),
    )
    return {
        str(port): status
        for port, status in zip(PORT_LIST, port_results, strict=True)
    }
