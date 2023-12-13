#!/bin/sh
set -e

sed "s/__JELLYFIN_DOMAIN__/$JELLYFIN_DOMAIN/g" /etc/caddy/Caddyfile > /etc/caddy/Caddyfile-live

exec /usr/bin/caddy run --config /etc/caddy/Caddyfile-live
