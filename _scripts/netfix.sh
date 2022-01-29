#!/bin/bash

set -eo pipefail

if [ -z "$1" ]
then
    SELF="$0"

    docker events --filter 'event=start' --format '{{.Actor.Attributes.name}}' | 
    while read -r container
    do
        "$SELF" "$container"
    done

    exit 0
fi

ID="$1"

if [ "$2" != "NSENTER" ]
then
    nsenter -n -t "$(docker inspect --format {{.State.Pid}} "$ID")" "$SELF" "$ID" "NSENTER"
fi

LAN_ROUTE="$(ip -4 route | grep '10\..*\.0\.0/16' | cut -d ' ' -f 1)"
if [ -z "$LAN_ROUTE"]
then
    exit 0
fi

LAN_GW="$(echo "$LAN_ROUTE" | sed s~.0/16~.1~)"

ip -4 route del default
ip -4 route add default via "$LAN_GW"
