#!/bin/sh
set -e

VERSION="v1.0.0"

rm -f /usr/local/bin/docker-sriov-plugin /usr/local/bin/ibdev2netdev
wget "https://raw.githubusercontent.com/Doridian/docker-sriov-plugin/$VERSION/ibdev2netdev" -O /usr/local/bin/ibdev2netdev
wget "https://github.com/Doridian/docker-sriov-plugin/releases/download/$VERSION/docker-sriov-plugin" -O /usr/local/bin/docker-sriov-plugin
chmod +x /usr/local/bin/docker-sriov-plugin /usr/local/bin/ibdev2netdev

systemctl enable docker-sriov-plugin
systemctl restart docker-sriov-plugin
