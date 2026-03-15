import socket

from app.config import PORT_LIST


async def check_ports() -> dict[str, str]:
    port_statuses: dict[str, str] = {}

    for port in PORT_LIST:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex(("127.0.0.1", port))
            port_statuses[str(port)] = "open" if result == 0 else "closed"

    return port_statuses
