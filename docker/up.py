#!/usr/bin/env python3

from os import chdir, listdir
from os.path import dirname, abspath
from subprocess import run
from sys import argv
from yaml import dump as yaml_dump
from tempfile import NamedTemporaryFile
from config import yaml_loadfile, DOCKER_COMPOSE_VERSION, HOST_CONFIG
from netgen import GLOBAL_NETWORKS

chdir(dirname(abspath(__file__)))
class ComposeProject():
    def __init__(self, name, project_dir):
        self.used_networks = set()
        self.provided_networks = set()
        self.name = name
        self.project_dir = project_dir
        self.files = set()

    def load_dir(self, dir):
        for filename in listdir(dir):
            if not filename.endswith(".yml"):
                continue
            file = f"{dir}/{filename}"
            self.add_yaml(file)

    def add_yaml(self, file):
        file = abspath(file)
        if file in self.files:
            return

        data = yaml_loadfile(file)
        if data["version"] != DOCKER_COMPOSE_VERSION:
            raise Exception(f"Unsupported compose file version: {data['version']}")

        if "services" in data:
            for service in data["services"]:
                self.add_service(service, data["services"][service])

        if "networks" in data:
            for network in data["networks"]:
                self.provided_networks.add(network)

        self.files.add(file)

    def add_service(self, _, data):
        if "networks" not in data:
            return
        for network in data["networks"]:
            if network == "default":
                continue
            self.used_networks.add(network)

    def get_missing_networks(self):
        return self.used_networks - self.provided_networks

    def deploy(self):
        if self.get_missing_networks():
            raise Exception(f"Missing network definitions for: {','.join(self.get_missing_networks())}")

        compose_args = ["docker-compose", "-p", self.name, "--project-directory", self.project_dir]
        for file in self.files:
            compose_args.append("-f")
            compose_args.append(file)
        
        run(compose_args + ["pull"])
        run(compose_args + ["up", "--build", "-d", "--remove-orphans"])

def load_role(role):
    if role == "":
        return
    print("Loading role", role)

    project = ComposeProject(role, role)
    project.load_dir(role)

    temp_file = None
    missing_networks = project.get_missing_networks()
    if missing_networks:
        used_global_nets = {
            "version": DOCKER_COMPOSE_VERSION,
            "networks": {
                network: GLOBAL_NETWORKS[network]
                for network in missing_networks
            }
        }
        temp_file = NamedTemporaryFile(mode="w+", suffix=".yml")
        yaml_dump(used_global_nets, temp_file)
        temp_file.flush()
        project.add_yaml(temp_file.name)

    project.deploy()
    if temp_file:
        temp_file.close()

def load_roles_by_hostname():
    roles = set(HOST_CONFIG['roles'])

    for role in roles:
        load_role(role.strip())

    run(["docker", "image", "prune", "-f", "-a"])

if len(argv) > 1:
    load_role(argv[1].strip())
else:
    load_roles_by_hostname()
