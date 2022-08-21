#!/usr/bin/env python3

from os import chdir, getenv, listdir
from os.path import dirname, abspath
from subprocess import run
from sys import argv
from typing import Container
from yaml import dump as yaml_dump
from tempfile import NamedTemporaryFile
from config import yaml_loadfile, HOST_CONFIG
from netgen import GLOBAL_NETWORKS, generate_dns_for_vlan
from dockermgr import Container, prune_images
from zlib import crc32

chdir(dirname(abspath(__file__)))

class ComposeProject():
    def __init__(self, name, project_dir, nopull, additional_config):
        self.used_networks = set()
        self.provided_networks = set()
        self.checked_containers = set()
        self.name = name
        self.project_dir = project_dir
        self.nopull = nopull
        self.needs_default_network = False
        self.files = set()
        self.additional_config = additional_config
        self.needs_additional_config = False

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
                self.additional_data["services"][service] = {}
                self.add_service(service, data["services"][service])

        if "networks" in data:
            for network in data["networks"]:
                self.provided_networks.add(network)

        self.files.add(file)

    def add_service(self, name, data):
        overrides_network = False
        has_dns = "dns" in data
        highest_priority_network = "default"
        highest_priority_network_priority = -1

        if "networks" in data:
            overrides_network = True
            for network in data["networks"]:
                net_priority = data["networks"].get("priority", 0)
                if net_priority > highest_priority_network_priority:
                    highest_priority_network = network
                    highest_priority_network_priority = net_priority

                if network == "default":
                    self.needs_default_network = True
                    continue
                self.used_networks.add(network)

        if "network_mode" in data:
            overrides_network = True
            self.checked_containers.add(name)

        if not has_dns:
            if highest_priority_network == "default":
                self.additional_data["services"][name]["dns"] = HOST_CONFIG["network"]["dns"]
                self.needs_additional_config = True
            elif highest_priority_network[:4] == "vlan":
                self.additional_data["services"][name]["dns"] = generate_dns_for_vlan(int(highest_priority_network[4:], 10))
                self.needs_additional_config = True

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

        compose_up_args = ["up"]
        if not self.nopull:
            run(compose_args + ["pull"])
            compose_up_args.append("--build")
        run(compose_args + compose_up_args + ["-d", "--remove-orphans"])

        for ct in self.checked_containers:
            print(f"Checking container {ct} in {self.name}")
            if not Container(f"{self.name}_{ct}_1").restart_if_failed():
                return self.deploy()

def load_role(role):
    if role == "":
        return
    print("Loading role", role)

    additional_config = {
        "services": {},
        "networks": {},
    }
    additional_config_needed = False

    project = ComposeProject(name=role, project_dir=role, nopull=(getenv("NOPULL", "").lower() == "yes"), additional_config=additional_config)
    project.load_dir(role)

    missing_networks = project.get_missing_networks()

    if project.needs_additional_config:
        additional_config_needed = True

    if missing_networks:
        additional_config_needed = True
        for network in missing_networks:
            additional_config["networks"][network] = GLOBAL_NETWORKS[network]

    if project.needs_default_network:
        additional_config_needed = True
        ula_base = HOST_CONFIG["network"]["ula_base"]
        ula_id = '{:x}'.format(crc32(role.encode()) & 0xFFFF)
        ula_subnet = f'{ula_base}{ula_id}:'

        additional_config["networks"]["default"] = {
            "enable_ipv6": True,
            "ipam": {
                "config": [
                    {
                        "subnet": f'{ula_subnet}:/64',
                        "gateway": f'{ula_subnet}:1'
                    }
                ]
            }
        }

    with NamedTemporaryFile(mode="w+", suffix=".yml") as temp_file:
        if additional_config_needed:
            yaml_dump(additional_config, temp_file)
            temp_file.flush()
            project.add_yaml(temp_file.name)

        project.deploy()

def load_roles_by_hostname():
    roles = set(HOST_CONFIG['roles'])

    for role in roles:
        load_role(role.strip())

def main():
    if len(argv) > 1:
        load_role(argv[1].strip())
    else:
        load_roles_by_hostname()

    prune_images()

if __name__ == "__main__":
    main()
