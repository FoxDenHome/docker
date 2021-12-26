#!/bin/sh
set -e

SHELL=/usr/bin/zsh
NOLOGIN=/usr/sbin/nologin

mktpluser() {
    addgroup -g "$2" "$1"
    adduser -D -s "$3" -G "$1" -u "$2" "$1"
}

mksysuser() {
    mktpluser "$1" "$2" "$NOLOGIN"
}

mknasuser() {
    mktpluser "$1" "$2" "$SHELL"
    adduser "$1" share

    mkdir -p "/etc/ssh/keys/$1"
    wget "https://raw.githubusercontent.com/Doridian/home-scripts/master/sshkeys/$1" -qO "/etc/ssh/keys/$1/list"
    chown -R "$1:$1" "/etc/ssh/keys/$1"
    chmod 700 "/etc/ssh/keys/$1"
    chmod 600 "/etc/ssh/keys/$1/list"
}

deluser guest || true
delgroup guest || true

mksysuser www-data 400
mksysuser smbauth  401
mksysuser guest    403
mksysuser share    1000
mknasuser doridian 1001
mknasuser wizzy    1002
