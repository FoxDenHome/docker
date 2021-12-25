from config import HOST_CONFIG

def generate_driver_opts(id, driver):
    if driver == "macvlan":
        return {
            "parent": f"br{id}",
        }
    elif driver == "sriov":
        cfg = {
            "netdevice": HOST_CONFIG["network"]["device"],
        }
        if id != HOST_CONFIG["network"]["pvid"]:
            cfg["vlan"] = f"{id}"
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
                    "subnet": f"192.168.{id}.0/24",
                    "gateway": f"192.168.{id}.6",
                },
            ],
        }
    }

GLOBAL_NETWORKS = {}
def load():
    global GLOBAL_NETWORKS
    GLOBAL_NETWORKS = {}
    for id in range(1, 9):
        net = generate_network_for_vlan(id)
        GLOBAL_NETWORKS[net["name"]] = net

load()
