#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

CONFIGS=""

load_role() {
    DIR="$1"
    for file in `find "$DIR" -type f -name '*.yml'`
    do
        CONFIGS="$CONFIGS -f $file"
    done
}

HN="$(hostname)"
for role in `cat "${HN}.roles"`
do
    load_role "$role"
done

docker-compose $CONFIGS up -d
