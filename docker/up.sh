#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

load_role() {
    CONFIGS=""
    DIR="$1"
    for file in `find "$DIR" -type f -name '*.yml'`
    do
        CONFIGS="$CONFIGS -f $file"
    done
    docker-compose $CONFIGS -f networks.yml up -d
}

HN="$(hostname)"
for role in `cat "${HN}.roles"`
do
    load_role "$role"
done
