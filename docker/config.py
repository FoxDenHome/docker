from socket import gethostname
from yaml import load as yaml_load
from yaml.loader import SafeLoader

def yaml_loadfile(file):
    fh = open(file, "r")
    data = yaml_load(fh, Loader=SafeLoader)
    fh.close()
    return data

HOST_CONFIG = yaml_loadfile(f"_config/{gethostname().lower()}.yml")
