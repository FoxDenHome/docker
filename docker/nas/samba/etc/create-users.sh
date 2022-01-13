#!/bin/sh
set -e

SHELL="$(which nologin)"
NOLOGIN="$(which nologin)"

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
}

deluser guest || true
delgroup guest || true

mksysuser guest    403
mksysuser share    1000
mknasuser doridian 1001
mknasuser wizzy    1002
