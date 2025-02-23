#!/bin/bash
set -euo pipefail

while :;
do
    echo '[MIRROR BEGIN]'
    /mirror.sh || echo "Exit code: $?"
    echo '[MIRROR END]'
    sleep 1h
done
