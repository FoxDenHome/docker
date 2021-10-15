#!/usr/bin/env python3

from os import chdir, listdir
from os.path import dirname, abspath
from socket import gethostname
from subprocess import run

chdir(dirname(abspath(__file__)))

def load_role(role):
    if role == "":
        return
    print("Loading role", role)
    compose_args = ["docker-compose", "-p", role]
    for file in listdir(role):
        if file.endswith(".yml"):
            compose_args.append("-f")
            compose_args.append(f"{role}/{file}")
    compose_args += ["-f", "networks.yml"]

    run(compose_args + ["pull"])
    run(compose_args + ["up", "-d", "--remove-orphans"])    

ROLES_FILE = f"{gethostname().lower()}.roles"

fh = open(ROLES_FILE, "r")
roles = fh.readlines()
fh.close()
for role in roles:
    load_role(role.strip())

run(["docker", "image", "prune", "-f", "-a"])

"""
load_role() {
    CONFIGS=""
    DIR="$1"
    for file in `find "$DIR" -type f -name '*.yml'`
    do
        CONFIGS="$CONFIGS -f $file"
    done
    ARGS="-p $DIR $CONFIGS -f networks.yml"
    docker-compose $ARGS pull
    docker-compose $ARGS up -d --remove-orphans
}

HN="$(hostname)"
for role in `cat "${HN}.roles"`
do
    load_role "$role"
done

docker image prune -f -a
"""
