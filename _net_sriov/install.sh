#!/bin/sh
set -ex

VERSION="1.4.4"
ARCH="amd64"

DIR="$(mktemp -d)"
cd "$DIR"

purge() {
    cd /
    rm -rf "$DIR"
}
purge_fail() {
    echo "Error: $1"
    purge
    exit 1
}

wget "https://github.com/FoxDenHome/docker-sriov-plugin/releases/download/$VERSION/docker-sriov-plugin-linux-$ARCH.tar.gz" -O artifact.tar.gz || purge_fail 'Downloading archive failed'
wget "https://github.com/FoxDenHome/docker-sriov-plugin/releases/download/$VERSION/docker-sriov-plugin-linux-$ARCH.tar.gz.sha256" -O artifact.tar.gz.sha256 || purge_fail 'Downloading checksum file failed'
(echo "$(cat artifact.tar.gz.sha256) artifact.tar.gz" | sha256sum -c) || purge_fail 'Checksum wrong'
tar -xvf artifact.tar.gz || purge_fail 'Could not unpack archive'

mvf() {
    DST="$1"
    SRC="$(basename "$DST")"
    if [ ! -f "$SRC" ]
    then
        purge_fail "Could not find: $SRC"
    fi
    rm -f "$DST" || purge_fail "Could not remove: $DST"
    mv "$SRC" "$DST" || purge_fail "Could not move $SRC to $DST"
}

mvf /usr/local/bin/docker-sriov-plugin
mvf /etc/systemd/system/docker-sriov-plugin.service

purge

systemctl daemon-reload
systemctl enable docker-sriov-plugin
systemctl restart docker-sriov-plugin
#systemctl restart docker
