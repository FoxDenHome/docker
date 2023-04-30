#!/usr/bin/env python3

from os import chdir, getenv, listdir, environ
from os.path import dirname, abspath
from subprocess import run, check_call
from sys import argv
from typing import Container
from yaml import dump as yaml_dump
from tempfile import NamedTemporaryFile
from config import yaml_loadfile, HOST_CONFIG
from netgen import GLOBAL_NETWORKS, generate_dns_for_vlan
from dockermgr import Container, prune_images
from zlib import crc32
from re import sub as re_sub

chdir(dirname(abspath(__file__)))

try:
    with open("/proc/driver/nvidia/version", "r") as f:
        environ["NVIDIA_DRIVER_VERSION"] = re_sub("\s+", " ", f.read()).split(" ")[7]
except FileNotFoundError:
    pass

DNS_SERVER = HOST_CONFIG["network"]["dns"]
PORT_MODE = HOST_CONFIG["network"]["portmode"]

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
        self.deploy_blocker_script = None

    def load_dir(self, dir):
        for filename in listdir(dir):
            file = f"{dir}/{filename}"

            if filename == "deploy_blocker" or filename.startswith("deploy_blocker."):
                self.deploy_blocker_script = file
                continue

            if not filename.endswith(".yml"):
                continue

            self.add_yaml(file)

    def add_yaml(self, file):
        file = abspath(file)
        if file in self.files:
            return

        data = yaml_loadfile(file)

        if "services" in data:
            for service in data["services"]:
                self.additional_config["services"][service] = {}
                self.add_service(service, data["services"][service])

        if "networks" in data:
            for network in data["networks"]:
                if PORT_MODE and network[:4] == "vlan":
                    continue
                self.additional_config["networks"][network] = {}
                self.provided_networks.add(network)

        tempfile = NamedTemporaryFile(mode="w+", suffix=".yml")
        tempfile.write(yaml_dump(data))
        self.files.add(tempfile)

    def add_service(self, name, data):
        overrides_network = False
        has_dns = "dns" in data
        highest_priority_network = "default"
        highest_priority_network_priority = -1

        if "networks" in data:
            overrides_network = True
            remove_networks = set()
            for netname, network in data["networks"].items():
                if PORT_MODE and netname[:4] == "vlan":
                    remove_networks.add(netname)
                    continue

                net_priority = network.get("priority", 0)
                if net_priority > highest_priority_network_priority:
                    highest_priority_network = netname
                    highest_priority_network_priority = net_priority

                if netname == "default":
                    self.needs_default_network = True
                    continue
                self.used_networks.add(netname)

                if not data.get("mac_address"):
                    raise ValueError(f"Missing mac_address for networked container {name}")

            for netname in remove_networks:
                data["networks"].pop(netname)

        if "ports" in data and not PORT_MODE:
                data.pop("ports")

        if "network_mode" in data:
            overrides_network = True
            has_dns = True
            self.checked_containers.add(name)

        if not has_dns:
            if highest_priority_network == "default":
                self.additional_config["services"][name]["dns"] = DNS_SERVER
                self.needs_additional_config = True
            elif highest_priority_network[:4] == "vlan":
                self.additional_config["services"][name]["dns"] = generate_dns_for_vlan(int(highest_priority_network[4:], 10))
                self.needs_additional_config = True

        if not overrides_network:
            self.needs_default_network = True

    def get_missing_networks(self):
        return self.used_networks - self.provided_networks

    def deploy_allowed(self):
        if self.deploy_blocker_script is None:
            return True

        res = run(self.deploy_blocker_script)
        return res.returncode == 0

    def deploy(self):
        if self.get_missing_networks():
            raise Exception(
                f"Missing network definitions for: {','.join(self.get_missing_networks())}")

        compose_args = ["docker-compose", "-p", self.name,
                        "--project-directory", self.project_dir]
        for file in self.files:
            compose_args.append("-f")
            compose_args.append(file.name)

        try:
            compose_up_args = ["up"]
            if not self.nopull:
                check_call(compose_args + ["pull"])
                compose_up_args.append("--build")
            check_call(compose_args + compose_up_args + ["-d", "--remove-orphans"])

            for ct in self.checked_containers:
                print(f"Checking container {ct} in {self.name}")
                if not Container(f"{self.name}_{ct}_1").restart_if_failed():
                    return self.deploy()
        finally:
            for file in self.files:
                file.close()
            self.files = []

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

    if not project.deploy_allowed():
        print("Deploy blocked for role", role)
        return

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
    roles = set(HOST_CONFIG["roles"])

    for role in roles:
        load_role(role.strip())

def main():
    if len(argv) > 1:
        load_role(argv[1].strip())
    else:
        load_roles_by_hostname()

    prune_images()

    if "post_scripts" in HOST_CONFIG:
        for script in HOST_CONFIG["post_scripts"]:
            check_call(script)

if __name__ == "__main__":
    main()
