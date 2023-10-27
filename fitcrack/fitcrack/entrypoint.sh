#!/bin/sh

set -ex

service cron start

exec ./entrypoint-fitcrack.sh
