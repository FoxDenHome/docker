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
