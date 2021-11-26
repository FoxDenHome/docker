#!/bin/sh
set -e

SHELL=/bin/zsh

adduser -s /bin/false -D -u 1000 share

mkuser() {
    adduser -s "$SHELL" -D -u "$2" "$1"
    adduser "$1" share
}

mkuser doridian 1001
mkuser wizzy    1002
