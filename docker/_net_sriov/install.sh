#!/bin/sh
set -e

VERSION="v1.0.1"

rm -f /usr/local/bin/docker-sriov-plugin /usr/local/bin/ibdev2netdev /etc/systemd/system/docker-sriov-plugin.service
wget "https://raw.githubusercontent.com/Doridian/docker-sriov-plugin/$VERSION/ibdev2netdev" -O /usr/local/bin/ibdev2netdev
wget "https://github.com/Doridian/docker-sriov-plugin/releases/download/$VERSION/docker-sriov-plugin" -O /usr/local/bin/docker-sriov-plugin
wget "https://raw.githubusercontent.com/Doridian/docker-sriov-plugin/$VERSION/ibdev2netdev" -O /etc/systemd/system/docker-sriov-plugin.service
chmod +x /usr/local/bin/docker-sriov-plugin /usr/local/bin/ibdev2netdev

systemctl enable docker-sriov-plugin
systemctl restart docker-sriov-plugin
