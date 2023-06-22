from config import HOST_CONFIG
from subprocess import check_call

VF_SCRIPT_PATH = "/var/sriov-init-script.sh"

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

VF_IF_MACS = {}

def load_vf_if_macs():
    try:
        with open(VF_SCRIPT_PATH, "r") as f:
            for line in f:
                if not line.startswith("#;[SAVE];"):
                    continue

                line_parse = line.strip().split(";")

                hostdev = line_parse[2]
                idx = int(line_parse[3], 10)
                mac_address = line_parse[4]

                if hostdev not in VF_IF_MACS:
                    VF_IF_MACS[hostdev] = {}
                VF_IF_MACS[hostdev][mac_address] = idx
    except FileNotFoundError:
        pass
load_vf_if_macs()


VF_SCRIPT_DATA = [
    "#!/bin/sh",
    "set -e",
]
def vf_cmd(cmd):
    check_call(["/bin/sh", "-c", cmd])
    VF_SCRIPT_DATA.append(cmd)

def net_grab_physical(netname, mac_address):
    driver = HOST_CONFIG["network"]["driver"]
    if driver != "sriov":
        return

    driver_opts = GLOBAL_NETWORKS[netname]["driver_opts"]
    vlan = driver_opts["vlan"]
    hostdev = HOST_CONFIG["network"]["device"]
    vfdev = HOST_CONFIG["network"]["vfdevice"]

    vf_if_local_macs: dict[str, int] = VF_IF_MACS.get(hostdev, {})
    VF_IF_MACS[hostdev] = vf_if_local_macs
    idx = vf_if_local_macs.get(mac_address, -1)
    if idx < 0:
        other_indices = set(vf_if_local_macs.values())
        idx = 0
        while idx in other_indices:
            idx += 1
        vf_if_local_macs[mac_address] = idx

    if idx == 0:
        vf_cmd(f"cat '/sys/class/net/{hostdev}/device/sriov_totalvfs' > '/sys/class/net/{hostdev}/device/sriov_numvfs'")

    vf_cmd(f"ip link set dev '{hostdev}' vf '{idx}' mac '{mac_address}' vlan '{vlan}' spoofchk on")
    vf_cmd(f"ip link set dev '{vfdev}v{idx}' address '{mac_address}' || true")
    VF_SCRIPT_DATA.append(f"#;[SAVE];{hostdev};{idx};{mac_address}")

def netgen_done():
    with open(VF_SCRIPT_PATH, "w") as f:
        f.write("\n".join(VF_SCRIPT_DATA))

GLOBAL_NETWORKS = {}
def load():
    global GLOBAL_NETWORKS
    GLOBAL_NETWORKS = {}
    for id in range(1, 9):
        net = generate_network_for_vlan(id)
        GLOBAL_NETWORKS[net["name"]] = net
load()
