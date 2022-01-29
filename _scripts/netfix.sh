#!/bin/bash

set -eo pipefail
SELF="$0"

if [ -z "$1" ]
then
    echo 'Checking all already running containers...'
    for CONTAINER in `docker ps --format '{{.Names}}'`
    do
        "$SELF" "$CONTAINER" || echo "Error checking $CONTAINER"
    done

    echo 'Hooking into docker events'
    docker events --filter 'event=start' --format '{{.Actor.Attributes.name}}' | 
    while read -r CONTAINER
    do
        "$SELF" "$CONTAINER" || echo "Error checking $CONTAINER"
    done

    exit 0
fi

CONTAINER="$1"

if [ "$2" != "NSENTER" ]
then
    nsenter -n -t "$(docker inspect --format {{.State.Pid}} "$CONTAINER")" "$SELF" "$CONTAINER" "NSENTER"
    exit 0
fi

echo -n "Checking $CONTAINER: "

LAN_ROUTE="$(ip -4 route | grep '10\..*\.0\.0/16' | cut -d' ' -f1 || true)"
if [ -z "$LAN_ROUTE" ]
then
    echo 'No LAN route found'
    exit 0
fi

LAN_GW="$(echo "$LAN_ROUTE" | sed s~.0/16~.1~)"

CURRENT_ROUTE="$(ip route get 8.8.8.8 | head -1)"
if echo "$CURRENT_ROUTE" | grep -vq 'dev eth'
then
    echo 'Route not via eth*, skipping'
    exit 0
fi

CURRENT_GW="$(echo "$CURRENT_ROUTE" | cut -d' ' -f3)"
if [ "$CURRENT_GW" = "$LAN_GW" ]
then
    echo 'Route already correct'
    exit 0
fi

ip -4 route del default
ip -4 route add default via "$LAN_GW"
echo 'Route adjusted'
