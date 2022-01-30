#!/usr/bin/env python3

from os import chdir, listdir
from os.path import dirname, abspath
from subprocess import run
from sys import argv
from typing import Container
from yaml import dump as yaml_dump
from tempfile import NamedTemporaryFile
from config import yaml_loadfile, HOST_CONFIG
from netgen import GLOBAL_NETWORKS
from dockermgr import Container, prune_images

chdir(dirname(abspath(__file__)))

class ComposeProject():
    def __init__(self, name, project_dir):
        self.used_networks = set()
        self.provided_networks = set()
        self.checked_containers = set()
        self.name = name
        self.project_dir = project_dir
        self.needs_default_network = False
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

        if "services" in data:
            for service in data["services"]:
                self.add_service(service, data["services"][service])

        if "networks" in data:
            for network in data["networks"]:
                self.provided_networks.add(network)

        self.files.add(file)

    def add_service(self, name, data):
        overrides_network = False

        if "networks" in data:
            overrides_network = True
            for network in data["networks"]:
                if network == "default":
                    self.needs_default_network = True
                    continue
                self.used_networks.add(network)

        if "network_mode" in data:
            overrides_network = True
            self.checked_containers.add(name)

        if not overrides_network:
            self.needs_default_network = True

    def get_missing_networks(self):
        return self.used_networks - self.provided_networks

    def deploy(self):
        if self.get_missing_networks():
            raise Exception(
                f"Missing network definitions for: {','.join(self.get_missing_networks())}")

        compose_args = ["docker-compose", "-p", self.name,
                        "--project-directory", self.project_dir]
        for file in self.files:
            compose_args.append("-f")
            compose_args.append(file)

        run(compose_args + ["pull"])
        run(compose_args + ["up", "--build", "-d", "--remove-orphans"])

        for ct in self.checked_containers:
            print(f"Checking container {ct} in {self.name}")
            Container(f"{self.name}_{ct}_1").restart_if_failed()

def load_role(role):
    if role == "":
        return
    print("Loading role", role)

    project = ComposeProject(role, role)
    project.load_dir(role)

    missing_networks = project.get_missing_networks()
    additional_config = {
        "networks": {}
    }

    if missing_networks:
        for network in missing_networks:
            additional_config["networks"][network] = GLOBAL_NETWORKS[network]

    if project.needs_default_network:
        ula_base = HOST_CONFIG["network"]["ula_base"]
        additional_config["networks"]["default"] = {
            "enable_ipv6": True,
            "ipam": {
                "config": [
                    {
                        "subnet": ula_base + ":/64",
                        "gateway": ula_base + "1:/64"
                    }
                ]
            }
        }

    temp_file = NamedTemporaryFile(mode="w+", suffix=".yml")
    yaml_dump(additional_config, temp_file)
    temp_file.flush()
    project.add_yaml(temp_file.name)

    project.deploy()

    temp_file.close()

def load_roles_by_hostname():
    roles = set(HOST_CONFIG['roles'])

    for role in roles:
        load_role(role.strip())

def main():
    if len(argv) > 1:
        load_role(argv[1].strip())
    else:
        load_roles_by_hostname()

    #prune_images()

if __name__ == "__main__":
    main()
