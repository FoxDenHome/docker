#!/bin/bash -e

export DISPLAY=":0"

/etc/addmodes.py

steam -tenfoot -steamos

echo "Session Running. Press [Return] to exit."
read

exit 0
