#!/usr/bin/env python3

# * * * * * /opt/docker/node-exporter.py /var/lib/prometheus/node-exporter/docker-custom.prom

from subprocess import check_output
from sys import argv
from os import rename, unlink
from json import loads as json_loads

DOCKER_STATUS_MAP = {
    "unknown": -2,
    "deleted": -1,

    "running": 1,
    "paused": 2,
    "restarting": 3,
    "oomkilled": 4,
    "dead": 5,
    "exited": 6,
    "created": 7,
}

DOCKER_HEALTH_STATUS_MAP = {
    "starting": 100,
    "healthy": 101,
    "unhealthy": 102,
}

def get_health_status(status: str) -> int | None:
    status = status.removeprefix("health:").strip()
    return DOCKER_HEALTH_STATUS_MAP.get(status, None)

def get_container_status(ct):
    if not ct:
        return DOCKER_STATUS_MAP["deleted"]

    base_status = ct["State"].lower()
    status = None
    if base_status == "running":
        base_health_status = ct["Status"].lower()
        if "(" in base_health_status:
            health_status = base_health_status.split("(", 2)[1].removesuffix(")").strip()
            status = get_health_status(health_status)
        elif base_health_status in DOCKER_HEALTH_STATUS_MAP:
            status = get_health_status(base_health_status)
        else:
            base_health_status = None

        if (not status) and base_health_status:
            print(f"Unknown health status: {health_status}")

    if not status:
        status = DOCKER_STATUS_MAP.get(base_status, DOCKER_STATUS_MAP["unknown"])
        if status == DOCKER_STATUS_MAP["unknown"]:
            print(f"Unknown status: {base_status.lower()}")

    return status

def get_prometheus_line(ct):
    status = get_container_status(ct)
    names = ct["Names"]
    if isinstance(names, list):
        names = names[0]
    return "docker_container_status{container=\"%s\"} %s" % (names, status)

def get_prometheus_header():
    return "# TYPE docker_container_status gauge"

def main():
    outfile = argv[1]
    tmpfile = f"{outfile}.tmp"

    data = check_output(["docker", "container", "list", "--all", "--format", "{{json .}}"]).splitlines()

    with open(tmpfile, "w") as fh:
        fh.write(get_prometheus_header())
        fh.write("\n")
        for ctjson in data:
            if not ctjson:
                continue
            ct = json_loads(ctjson)
            fh.write(get_prometheus_line(ct))
            fh.write("\n")

    try:
        unlink(outfile)
    except:
        pass
    rename(tmpfile, outfile)

if __name__ == "__main__":
    main()
