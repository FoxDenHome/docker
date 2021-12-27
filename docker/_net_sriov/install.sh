#!/bin/sh
set -ex

VERSION="1.4.1"
ARCH="amd64"

DIR="$(mktemp -d)"
cd "$DIR"

purge() {
    cd /
    rm -rf "$DIR"
}
purge_fail() {
    purge
    exit 1
}

wget "https://github.com/Doridian/docker-sriov-plugin/releases/download/$VERSION/docker-sriov-plugin-linux-$ARCH.tar.gz" -O artifact.tar.gz || purge_fail
tar -xvf artifact.tar.gz || purge_fail

mvf() {
    DST="$1"
    SRC="$(basename "$DST")"
    if [ ! -f "$SRC" ]
    then
        echo "Could not find: $SRC"
        purge_fail
    fi
    rm -f "$DST" || purge_fail
    mv "$SRC" "$DST" || purge_fail
}

mvf /usr/local/bin/docker-sriov-plugin
mvf /etc/systemd/system/docker-sriov-plugin.service

purge

systemctl daemon-reload
systemctl enable docker-sriov-plugin
systemctl restart docker-sriov-plugin
#systemctl restart docker
