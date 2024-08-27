#!/bin/bash

while :; do
    # Sleep between 0 minutes and 60 minutes before starting the sync
    NEXTSLEEP=$[RANDOM%60]
    echo "[LOOP] Pre-Sleeping for ${NEXTSLEEP} minutes"
    sleep ${NEXTSLEEP}m

    echo '[LOOP] Running /sync.sh'
    /sync.sh
    ECODE=$?
    echo "[LOOP] Sync completed with code: ${ECODE}"

    # Slep at least until the next full hour (1 minute to make sure)
    NEXTSLEEP=$((61 - $(date +%M)))
    echo "[LOOP] Post-Sleeping for ${NEXTSLEEP} minutes until the next full hour"
    sleep ${NEXTSLEEP}m
done
