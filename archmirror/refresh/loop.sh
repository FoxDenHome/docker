#!/bin/bash

while :; do
    # Sleep between 0 minutes and 60 minutes before starting the sync
    NEXTSLEEP=$[RANDOM%60]
    echo "Pre-Sleeping for ${NEXTSLEEP} minutes"
    sleep ${NEXTSLEEP}m

    /sync.sh

    echo "Sleeping for 180 minutes"
    sleep 180m
done
