from config import HOST_CONFIG
from subprocess import check_call

def get_hostdev_for(id):
    vlan_dev = f"vlan{id}"
    if vlan_dev in HOST_CONFIG["network"]:
        return HOST_CONFIG["network"][vlan_dev]

    host_dev = HOST_CONFIG["network"]["device"]
    if host_dev:
        if id == HOST_CONFIG["network"]["pvid"]:
            return f"{host_dev}"
        return f"{host_dev}.{id}"
    return f"br{id}"

def generate_driver_opts(id, driver):
    if driver == "macvlan":
        return {
            "parent": get_hostdev_for(id),
        }
    elif driver == "sriov":
        cfg = {
            "netdevice": HOST_CONFIG["network"]["device"],
            "prefix": "eth",
            "mode": "sriov",
        }
        if id != HOST_CONFIG["network"]["pvid"]:
            cfg["vlan"] = f"{id}"
        else:
            cfg["vlan"] = "0"
        return cfg
    elif driver == "bridge":
        cfg = {
            "com.docker.network.bridge.name": get_hostdev_for(id),
            "com.docker.network.bridge.enable_ip_masquerade": "false",
            "com.docker.network.bridge.inhibit_ipv4": "true",
        }
        if "mtu" in HOST_CONFIG["network"]:
            mtu = HOST_CONFIG["network"]["mtu"]
            cfg["com.docker.network.driver.mtu"] = f"{mtu}"
        return cfg
    else:
        raise ValueError(f"Invalid net_driver {driver}")

def generate_network_for_vlan(id):
    driver = HOST_CONFIG["network"]["driver"]
    return {
        "name": f"vlan{id}",
        "driver": driver,
        "driver_opts": generate_driver_opts(id, driver),
        "ipam": {
            "driver": "default",
            "config": [
                {
                    "subnet": f"10.{id}.0.0/16",
                    "gateway": f"10.{id}.0.1",
                },
            ],
        }
    }

def generate_dns_for_vlan(id):
    return [
        f"10.{id}.0.53"
    ]

VF_MIN_IDS = {}
VF_USED_MACS = {}

VF_SCRIPT = open("/var/sriov-init-script.sh", "w")
VF_SCRIPT.write("#!/bin/sh\nset -e\n")
VF_SCRIPT.flush()
def vf_cmd(cmd):
    check_call(["/bin/sh", "-c", cmd])
    VF_SCRIPT.write(f"{cmd}\n")
    VF_SCRIPT.flush()

def net_grab_physical(netname, mac_address):
    if VF_USED_MACS.get(mac_address, False):
        raise ValueError(f"Duplicate MAC: {mac_address}")
    VF_USED_MACS[mac_address] = True

    driver = HOST_CONFIG["network"]["driver"]
    if driver != "sriov":
        return

    driver_opts = GLOBAL_NETWORKS[netname]["driver_opts"]
    vlan = driver_opts["vlan"]
    hostdev = driver_opts["netdevice"]

    idx = VF_MIN_IDS.get(hostdev, 0)
    if idx == 0:
        vf_cmd(f"cat '/sys/class/net/{hostdev}/device/sriov_totalvfs' > '/sys/class/net/{hostdev}/device/sriov_numvfs'")
    VF_MIN_IDS[hostdev] = idx + 1

    vf_cmd(f"ip link set '{hostdev}' vf '{idx}' mac '{mac_address}' vlan '{vlan}' spoofchk on")

GLOBAL_NETWORKS = {}
def load():
    global GLOBAL_NETWORKS
    GLOBAL_NETWORKS = {}
    for id in range(1, 9):
        net = generate_network_for_vlan(id)
        GLOBAL_NETWORKS[net["name"]] = net
load()
