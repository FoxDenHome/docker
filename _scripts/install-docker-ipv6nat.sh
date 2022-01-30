#!/bin/sh
set -e

VERSION="v0.4.4"
ARCH="amd64"

DIR="$(mktemp -d)"
purge() {
    cd /
    rm -rf "$DIR"
}
purge_fail() {
    echo "Error: $1"
    purge
    exit 1
}

cp "$(dirname "$0")"/docker-ipv6nat.service /etc/systemd/system/docker-ipv6nat.service || purge_fail 'Error copying systemd service'

cd "$DIR"

wget "https://github.com/robbertkl/docker-ipv6nat/releases/download/$VERSION/docker-ipv6nat.$ARCH" -O docker-ipv6nat || purge_fail 'Error downloading binary'
chmod +x docker-ipv6nat || purge_fail 'Error setting permissions'

rm -f /usr/local/sbin/docker-ipv6nat || purge_fail 'Error removing old binary'
cp docker-ipv6nat /usr/local/sbin/docker-ipv6nat || purge_fail 'Error copying new binary'

systemctl enable --now docker-ipv6nat || purge_fail 'Error enabling service'

purge
