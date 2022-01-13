#!/bin/sh

envsubst < /Caddyfile.tpl > /Caddyfile
exec /caddy run --config /Caddyfile