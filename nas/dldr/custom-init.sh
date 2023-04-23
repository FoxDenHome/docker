#!/bin/bash
set -e

rm -rf /config/plugins
ln -sf /plugins /config/plugins

exec /usr/local/bin/init.sh
