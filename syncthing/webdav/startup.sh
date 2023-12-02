#!/bin/sh
set -e

sed "s~__SYNCTHING_DOMAIN__~${SYNCTHING_DOMAIN}~g" /etc/caddy/Caddyfile.tpl > /etc/caddy/Caddyfile

exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
