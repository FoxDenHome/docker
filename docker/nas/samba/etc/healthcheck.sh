#!/bin/sh
set -e

curl -s -f "http://${HOSTNAME}/__/healthcheck"
smbstatus -S -f
