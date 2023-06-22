#!/bin/sh
set -e

VERSION="1.5.0"

rm -f /usr/local/bin/docker-sriov-plugin /etc/systemd/system/docker-sriov-plugin.service /tmp/sriov-plugin.tar.gz
wget "https://github.com/FoxDenHome/docker-sriov-plugin/releases/download/$VERSION/docker-sriov-plugin-linux-amd64.tar.gz" -O /tmp/sriov-plugin.tar.gz
tar -C /usr/local/bin -xvf /tmp/sriov-plugin.tar.gz
mv /usr/local/bin/docker-sriov-plugin.service /etc/systemd/system/docker-sriov-plugin.service
rm -f /usr/local/bin/LICENSE /usr/local/bin/README.md
chmod +x /usr/local/bin/docker-sriov-plugin

sed 's~Restart=always~Restart=always\nExecStartPre=-/bin/sh /var/sriov-init-script.sh'

systemctl daemon-reload
systemctl enable docker-sriov-plugin
systemctl restart docker-sriov-plugin
