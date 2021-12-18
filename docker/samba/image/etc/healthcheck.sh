#!/bin/sh
set -e

curl -s -f "http://${HOSTNAME}/__healthcheck"
smbstatus -S -f
