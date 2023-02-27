#!/bin/bash -e

export SEATD_VTBOUND=0
export WLR_LIBINPUT_NO_DEVICES=1
unset DISPLAY

eval "$(dbus-launch --auto-syntax)"

pipewire &
sleep 1

gamescope -W 3840 -H 1600 -w 3840 -h 1600 -r 60 -e -- steam -tenfoot -steamos -pipewire-dmabuf

echo "Session Running. Press [Return] to exit."
read

exit 0
