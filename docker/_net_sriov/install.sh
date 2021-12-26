#!/bin/sh
set -ex

VERSION="1.2.0"
ARCH="amd64"

DIR="$(mktemp -d)"
cd "$DIR"

wget "https://github.com/Doridian/docker-sriov-plugin/releases/download/$VERSION/docker-sriov-plugin-linux-$ARCH.tar.gz" -O artifact.tar.gz
tar -xvf artifact.tar.gz

mvf() {
    DST="$1"
    SRC="$(basename "$DST")"
    rm -f "$DST"
    mv "$SRC" "$DST"
}

mvf /usr/local/bin/docker-sriov-plugin
mvf /usr/local/bin/ibdev2netdev
mvf /etc/systemd/system/docker-sriov-plugin.service

cd /
rm -rf "$DIR"

systemctl daemon-reload
systemctl enable docker-sriov-plugin
systemctl restart docker-sriov-plugin
