#!/bin/sh
set -e

SHELL=/usr/bin/zsh
NOLOGIN=/usr/sbin/nologin

mksysuser() {
    groupadd -g "$2" "$1"
    useradd -p '*' --shell "$NOLOGIN" --gid "$2" --uid "$2" "$1"
}

mknasuser() {
    groupadd -g "$2" "$1"
    useradd -p '*' --shell "$SHELL" --gid "$2" --uid "$2" "$1"
    adduser "$1" share
}

mksysuser smbauth  401
mksysuser guest    403
mksysuser share    1000
mknasuser doridian 1001
mknasuser wizzy    1002
