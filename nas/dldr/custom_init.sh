#!/bin/bash
set -e

/home/nobody/config_deluge.py "/config/core.conf" "plugins_location" "/plugins"
/config_deluge_type.py "/config/core.conf" "enabled_plugins" "Pieces" "array"

exec /usr/local/bin/init.sh
