#!/bin/bash
set -e

/home/nobody/config_deluge.py "/config/core.conf" "plugins_location" "/plugins"
/home/nobody/config_deluge_array.py "/config/core.conf" "enabled_plugins" "Pieces"

exec /usr/local/bin/init.sh
