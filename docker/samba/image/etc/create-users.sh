#!/bin/sh
set -e

SHELL=/usr/bin/zsh
NOLOGIN=/usr/sbin/nologin

mktpluser() {
    groupadd -g "$2" "$1"
    useradd -p '*' --shell "$3" --gid "$2" --uid "$2" "$1"
}

mksysuser() {
    mktpluser "$1" "$2" "$NOLOGIN"
}

mknasuser() {
    mktpluser "$1" "$2" "$SHELL"
    adduser "$1" share

    mkdir -p "/etc/ssh/keys/$1"

    chown -R "$1:$1" "/etc/ssh/keys/$1"
    wget "https://raw.githubusercontent.com/Doridian/home-scripts/master/sshkeys/$1" -qO "/etc/ssh/keys/$1/list"
    chmod 700 "/etc/ssh/keys/$1"
    chmod 600 "/etc/ssh/keys/$1/list"
}

mksysuser smbauth  401
mksysuser guest    403
mksysuser share    1000
mknasuser doridian 1001
mknasuser wizzy    1002
