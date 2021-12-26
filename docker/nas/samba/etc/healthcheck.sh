#!/bin/sh
set -e

curl -s -f "http://${HOSTNAME}:8888/__healthcheck"
smbstatus -S -f
