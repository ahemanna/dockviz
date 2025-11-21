from datetime import datetime

import docker

client = docker.from_env()

def get_port_mappings():
    containers = client.containers.list()
    results = []
    for container in containers:
        info = container.attrs
        ports = info["NetworkSettings"]["Ports"] or {}

        image = info["Config"]["Image"]
        status = info["State"]["Status"]
        created = info["Created"]
        started = info["State"]["StartedAt"]
        labels = info["Config"].get("Labels", {})
        networks = list(info["NetworkSettings"]["Networks"].keys())

        for container_port, mappings in ports.items():
            port_number, protocol = container_port.split("/")
            if mappings:
                for mapping in mappings:
                    results.append({
                        "container": container.name,
                        "image": image,
                        "status": status,
                        "created": format_created_time(created),
                        "started": format_created_time(started),
                        "network": networks,
                        "container_port": port_number,
                        "protocol": protocol,
                        "host_ip": mapping.get("HostIp"),
                        "host_port": mapping.get("HostPort")
                    })
            else:
                results.append({
                    "container": container.name,
                    "image": image,
                    "status": status,
                    "created": created,
                    "started": started,
                    "network": networks,
                    "container_port": port_number,
                    "protocol": protocol,
                    "host_ip": "-",
                    "host_port": "-"
                })

    return results

def format_created_time(ts):
    ts = ts.rstrip("Z")
    if "." in ts:
        base, frac = ts.split(".")
        frac = frac[:6]
        ts = f"{base}.{frac}"
    dt = datetime.fromisoformat(ts)
    return dt.strftime("%d %b %Y, %H:%M")
