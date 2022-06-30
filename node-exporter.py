#!/usr/bin/env python3

# * * * * * /opt/docker/node-exporter.py > /var/lib/prometheus/node-exporter/docker-custom.prom

from docker import DockerClient

DOCKER_STATUS_MAP = {
    "unknown": -2,
    "deleted": -1,

    "running": 1,
    "paused": 2,
    "restarting": 3,
    "oomkilled": 4,
    "dead": 5,
}

DOCKER_HEALTH_STATUS_MAP = {
    "starting": 100,
    "healthy": 101,
    "unhealthy": 102,
}

def get_container_status(ct):
    if not ct:
        return DOCKER_STATUS_MAP["deleted"]

    state = ct.attrs["State"]
    status = None
    
    if "Health" in state:
        health_status = state["Health"]["Status"]
        status = DOCKER_HEALTH_STATUS_MAP.get(health_status, None)

    if not status:
        status = DOCKER_STATUS_MAP.get(state["Status"], DOCKER_STATUS_MAP["unknown"])

    return status

def get_prometheus_line(ct):
    status = get_container_status(ct)
    return "docker_container_status{container=\"%s\"} %s" % (ct.name, status)

def get_prometheus_header():
    return "# TYPE docker_container_status gauge"

def main():
    client = DockerClient(base_url="unix://var/run/docker.sock")
    print(get_prometheus_header())
    for ct in client.containers.list():
        print(get_prometheus_line(ct))

if __name__ == "__main__":
    main()
