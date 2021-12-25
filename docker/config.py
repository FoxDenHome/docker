from os import chdir, listdir
from os.path import dirname, abspath
from socket import gethostname
from subprocess import run
from sys import argv
from yaml import load as yaml_load, dump as yaml_dump
from yaml.loader import SafeLoader
from tempfile import NamedTemporaryFile
from netgen import generate_network_for_vlan

def yaml_loadfile(file):
    fh = open(file, "r")
    data = yaml_load(fh, Loader=SafeLoader)
    fh.close()
    return data

DOCKER_COMPOSE_VERSION = "2.4"
HOST_CONFIG = yaml_loadfile(f"_config/{gethostname().lower()}.yml")
