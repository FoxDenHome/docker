def generate_driver_opts(id, driver):
    if driver == 'macvlan':
        return {
            "parent": f"br{id}",
        }

def generate_network_for_vlan(id, driver='macvlan'):
    return {
        "name": f"vlan{id}",
        "driver": driver,
        "driver_opts": generate_driver_opts(driver, id),\
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
