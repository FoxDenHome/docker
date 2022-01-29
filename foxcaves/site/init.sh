#!/bin/sh

set -e
ip route del default
ip route add default via 10.3.0.1

exec s6-svscan /etc/s6