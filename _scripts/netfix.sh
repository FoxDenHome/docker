#!/bin/bash

set -eo pipefail

if [ -z "$1" ]
then
    SELF="$0"

    docker events --filter 'event=start' --format '{{.Actor.Attributes.name}}' | 
    while read -r container
    do
        nsenter -n -t "$(docker inspect --format {{.State.Pid}} "$container")" "$SELF" "$container"
    done

    exit 0
fi

ID="$1"

ip route
