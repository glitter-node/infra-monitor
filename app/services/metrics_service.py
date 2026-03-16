from prometheus_client import CollectorRegistry, Gauge, generate_latest

from app.services.status_service import aggregate_status


async def generate_metrics() -> str:
    status = await aggregate_status()
    registry = CollectorRegistry()

    memory_percent = Gauge(
        "infra_memory_percent",
        "System memory usage percentage",
        registry=registry,
    )
    disk_percent = Gauge(
        "infra_disk_percent",
        "System disk usage percentage",
        registry=registry,
    )
    port_open = Gauge(
        "infra_port_open",
        "Infrastructure port open state",
        labelnames=("port",),
        registry=registry,
    )
    port_closed = Gauge(
        "infra_port_closed",
        "Infrastructure port closed state",
        labelnames=("port",),
        registry=registry,
    )
    upstream_running = Gauge(
        "infra_upstream_running",
        "Upstream running state",
        labelnames=("target",),
        registry=registry,
    )
    upstream_down = Gauge(
        "infra_upstream_down",
        "Upstream down state",
        labelnames=("target",),
        registry=registry,
    )
    service_running = Gauge(
        "infra_service_running",
        "DSM service running state",
        labelnames=("port",),
        registry=registry,
    )
    service_down = Gauge(
        "infra_service_down",
        "DSM service down state",
        labelnames=("port",),
        registry=registry,
    )

    system = status["system"]
    if system:
        memory_percent.set(float(system.get("memory_percent", 0.0)))
        disk_percent.set(float(system.get("disk_percent", 0.0)))

    for port, port_status in status["ports"].items():
        if port_status == "open":
            port_open.labels(port=port).set(1)
        else:
            port_closed.labels(port=port).set(1)

    for target, upstream_status in status["upstreams"].items():
        if upstream_status == "running":
            upstream_running.labels(target=target).set(1)
        else:
            upstream_down.labels(target=target).set(1)

    for port, service_status in status["services"].items():
        if service_status == "running":
            service_running.labels(port=port).set(1)
        else:
            service_down.labels(port=port).set(1)

    return generate_latest(registry).decode("utf-8")
