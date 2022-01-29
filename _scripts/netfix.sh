#!/bin/bash

set -euo pipefail

if [ -z "$1" ]
then
    SELF="$0"

    docker events --filter 'event=start' --format '{{.Actor.Attributes.name}}' | 
    while read -r container
    do
        $SELF "$container"
    done
    exit 0
fi

ID="$1"

