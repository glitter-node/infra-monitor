function formatBytes(bytes) {
    if (!Number.isFinite(bytes)) {
        return "-";
    }

    const units = ["B", "KB", "MB", "GB", "TB", "PB"];
    let value = bytes;
    let unitIndex = 0;

    while (value >= 1024 && unitIndex < units.length - 1) {
        value /= 1024;
        unitIndex += 1;
    }

    return `${value.toFixed(value >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
}

function formatUptime(seconds) {
    if (!Number.isFinite(seconds)) {
        return "-";
    }

    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    const parts = [];
    if (days > 0) {
        parts.push(`${days}d`);
    }
    if (hours > 0 || days > 0) {
        parts.push(`${hours}h`);
    }
    parts.push(`${minutes}m`);
    return parts.join(" ");
}

function formatLoadAverage(loadAverage) {
    if (!Array.isArray(loadAverage) || loadAverage.length === 0) {
        return "-";
    }

    return loadAverage.map((value) => Number(value).toFixed(2)).join(" / ");
}

function createStatusRow(name, status, healthyValues) {
    const isHealthy = healthyValues.includes(status);
    const row = document.createElement("article");
    row.className = "status-item";

    const info = document.createElement("div");
    info.className = "status-info";

    const indicator = document.createElement("span");
    indicator.className = `status-indicator ${isHealthy ? "status-healthy" : "status-failure"}`;

    const labelGroup = document.createElement("div");

    const title = document.createElement("div");
    title.className = "status-name";
    title.textContent = name;

    const meta = document.createElement("div");
    meta.className = "status-meta";
    meta.textContent = isHealthy ? "Healthy" : "Attention needed";

    labelGroup.appendChild(title);
    labelGroup.appendChild(meta);

    info.appendChild(indicator);
    info.appendChild(labelGroup);

    const value = document.createElement("div");
    value.className = `status-value ${isHealthy ? "status-healthy" : "status-failure"}`;
    value.textContent = status;

    row.appendChild(info);
    row.appendChild(value);
    return row;
}

function renderStatusSection(containerId, data, healthyValues) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    const entries = Object.entries(data || {});
    if (entries.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "No data available";
        container.appendChild(empty);
        return;
    }

    entries.forEach(([name, status]) => {
        container.appendChild(createStatusRow(name, status, healthyValues));
    });
}

function updateSystem(system) {
    document.getElementById("system-hostname").textContent = system.hostname || "-";
    document.getElementById("system-uptime").textContent = formatUptime(system.uptime_seconds);
    document.getElementById("system-memory").textContent =
        `${Number(system.memory_percent ?? 0).toFixed(1)}% of ${formatBytes(system.memory_total)}`;
    document.getElementById("system-disk").textContent =
        `${Number(system.disk_percent ?? 0).toFixed(1)}% of ${formatBytes(system.disk_total)}`;
    document.getElementById("system-load").textContent = formatLoadAverage(system.load_average);
}

function updateLastUpdated() {
    const timestamp = new Date();
    document.getElementById("last-updated").textContent = timestamp.toLocaleString();
}

async function refreshDashboard() {
    try {
        const response = await fetch("/api/status", {
            headers: {
                Accept: "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        updateSystem(data.system || {});
        renderStatusSection("ports-list", data.ports, ["open"]);
        renderStatusSection("upstreams-list", data.upstreams, ["running"]);
        renderStatusSection("services-list", data.services, ["running"]);
        updateLastUpdated();
    } catch (error) {
        document.getElementById("last-updated").textContent = `Refresh failed: ${error.message}`;
    }
}

refreshDashboard();
setInterval(refreshDashboard, 5000);
