#!/usr/bin/env python3

# * * * * * /opt/docker/node-exporter.py /var/lib/prometheus/node-exporter/docker-custom.prom

from docker import DockerClient
from sys import argv
from os import rename, unlink

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

    base_status = state["Status"].lower()
    
    if base_status == "running" and "Health" in state:
        health_status = state["Health"]["Status"].lower()
        status = DOCKER_HEALTH_STATUS_MAP.get(health_status, None)

    if not status:
        status = DOCKER_STATUS_MAP.get(base_status, DOCKER_STATUS_MAP["unknown"])

    return status

def get_prometheus_line(ct):
    status = get_container_status(ct)
    return "docker_container_status{container=\"%s\"} %s" % (ct.name, status)

def get_prometheus_header():
    return "# TYPE docker_container_status gauge"

def main():
    outfile = argv[1]
    tmpfile = f"{outfile}.tmp"

    client = DockerClient(base_url="unix://var/run/docker.sock")

    with open(tmpfile, "w") as fh:
        fh.write(get_prometheus_header())
        fh.write("\n")
        for ct in client.containers.list():
            fh.write(get_prometheus_line(ct))
            fh.write("\n")

    try:
        unlink(outfile)
    except:
        pass
    rename(tmpfile, outfile)

if __name__ == "__main__":
    main()