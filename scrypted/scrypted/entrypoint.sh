#!/bin/sh
set -ex

dbus-uuidgen > /var/lib/dbus/machine-id
dbus-daemon --config-file=/usr/share/dbus-1/system.conf --print-address
avahi-daemon --daemonize

exec npm --prefix /server exec scrypted-serve
