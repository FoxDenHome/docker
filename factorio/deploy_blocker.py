#!/usr/bin/env python3
exit(0)

from subprocess import check_output
import factorio_rcon

rcon_pw = None
with open("/var/lib/docker/231072.231072/volumes/factorio_data/_data/config/rconpw", "r") as fh:
    rcon_pw = fh.read().strip()

try:
    server_ip = check_output(["docker", "inspect", "-f", "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}", "factorio-server-1"]).strip()
except:
    exit(0)

client = factorio_rcon.RCONClient(server_ip, 27015, rcon_pw)
response = client.send_command("/players")

if "Players (" not in response:
    print("Invalid response:")
    print(response)
    exit(2)

has_players = "(online)" in response

if has_players:
    exit(1)
