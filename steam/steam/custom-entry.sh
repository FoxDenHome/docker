#!/bin/bash -e

pipewire &
sleep 1

gamescope -W 3840 -H 1600 -r 60 -f -e -- steam -gamepadui

echo "Session Running. Press [Return] to exit."
read
exit 0
