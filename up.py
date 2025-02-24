#!/usr/bin/env python3

from os import chdir, getenv, listdir, environ
from os.path import dirname, abspath, exists
from subprocess import run, check_call
from sys import argv
from typing import Container
from yaml import dump as yaml_dump
from tempfile import NamedTemporaryFile
from config import yaml_loadfile, HOST_CONFIG, HOST_NAME
from netgen import GLOBAL_NETWORKS, generate_dns_for_vlan, net_grab_physical, netgen_done
from dockermgr import Container, prune_images
from zlib import crc32
from re import sub as re_sub
from dataclasses import dataclass

chdir(dirname(abspath(__file__)))

try:
    with open("/proc/driver/nvidia/version", "r") as f:
        environ["NVIDIA_DRIVER_VERSION"] = re_sub("\\s+", " ", f.read()).split(" ")[7]
except FileNotFoundError:
    pass

DNS_SERVER = HOST_CONFIG["network"]["dns"]

@dataclass
class Service():
    name: str
    has_dns: bool
    needs_default_network: bool
    overrides_network: bool
    highest_priority_network: str
    highest_priority_network_priority: int


class ComposeProject():
    services: dict[str, Service]

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
        self.services = {}

    def load_dir(self, dir):
        for filename in sorted(listdir(dir)):
            file = f"{dir}/{filename}"

            if filename == "deploy_blocker" or filename.startswith("deploy_blocker."):
                self.deploy_blocker_script = file
                continue

            if not filename.endswith(".yml"):
                continue

            self.add_yaml(file)

        override_file = f"{dir}/_overrides/{HOST_NAME}.yml"
        if exists(override_file):
            self.add_yaml(override_file)

        self.finalize()

    def finalize(self):
        for name in sorted(self.services):
            svc = self.services[name]
            if not svc.overrides_network:
                svc.needs_default_network = True

            if svc.needs_default_network:
                self.needs_default_network = True

            if not svc.has_dns:
                if svc.highest_priority_network[:4] == "vlan":
                    self.additional_config["services"][svc.name]["dns"] = generate_dns_for_vlan(int(svc.highest_priority_network[4:], 10))
                    self.needs_additional_config = True
                elif svc.highest_priority_network is not None:
                    self.additional_config["services"][svc.name]["dns"] = DNS_SERVER
                    self.needs_additional_config = True

    def add_yaml(self, file):
        file = abspath(file)
        if file in self.files:
            return

        data = yaml_loadfile(file)

        if "networks" in data:
            for network in sorted(data["networks"]):
                self.provided_networks.add(network)

        if "services" in data:
            for service in sorted(data["services"]):
                self.additional_config["services"][service] = {}
                self.add_service(service, data["services"][service])

        self.files.add(file)

    def add_service(self, name, data):
        svc = self.services.get(name, None)
        if svc is None:
            svc = Service(
                name=name,
                has_dns=False,
                needs_default_network=False,
                overrides_network=False,
                highest_priority_network="default",
                highest_priority_network_priority=-1,
            )
            self.services[name] = svc

        if "dns" in data:
            svc.has_dns = True

        if "networks" in data:
            svc.overrides_network = True
            for netname, network in sorted(data["networks"].items()):
                net_priority = network.get("priority", 0)
                if net_priority > svc.highest_priority_network_priority:
                    svc.highest_priority_network = netname
                    svc.highest_priority_network_priority = net_priority

                if netname == "default":
                    svc.needs_default_network = True
                    continue

                self.used_networks.add(netname)
                if "mac_address" in network:
                    net_grab_physical(netname, network["mac_address"])

        if "network_mode" in data:
            svc.overrides_network = True
            svc.has_dns = True
            self.checked_containers.add(name)

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

        compose_args = ["docker", "compose", "-p", self.name,
                        "--project-directory", self.project_dir]
        for file in sorted(self.files):
            compose_args.append("-f")
            compose_args.append(file)

        compose_up_args = ["up"]
        if not self.nopull:
            check_call(compose_args + ["pull"])
            compose_up_args.append("--build")
        check_call(compose_args + compose_up_args + ["-d", "--remove-orphans"])

        for ct in sorted(self.checked_containers):
            print(f"Checking container {ct} in {self.name}")
            if not Container(f"{self.name}-{ct}-1").restart_if_failed():
                return self.deploy()

def load_role(role, deploy):
    if role == "":
        return
    print("Loading role", role, deploy)

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
        for network in sorted(missing_networks):
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

    if not deploy:
        return

    with NamedTemporaryFile(mode="w+", suffix=".yml") as temp_file:
        if additional_config_needed:
            yaml_dump(additional_config, temp_file)
            temp_file.flush()
            project.add_yaml(temp_file.name)

        project.deploy()

def load_roles_by_hostname(deployfn=None):
    roles = set(HOST_CONFIG["roles"])

    for role in sorted(roles):
        role = role.strip()
        load_role(role, deployfn(role))

def deploy_all(role: str):
    return True

def make_deploy_set(roles: set[str]):
    def deployfn(role: str):
        return role.lower() in roles
    return deployfn

def main():
    deployfn = deploy_all
    if len(argv) > 1:
        deployfn = make_deploy_set(set([x.strip().lower() for x in argv[1:]]))

    load_roles_by_hostname(deployfn)
    netgen_done()
    prune_images()

    if "post_scripts" in HOST_CONFIG:
        for script in HOST_CONFIG["post_scripts"]:
            check_call(script)

if __name__ == "__main__":
    main()
