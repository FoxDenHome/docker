#!/bin/sh
set -e

sed "s~__HOMEASSISTANT_API_TOKEN__~$HOMEASSISTANT_API_TOKEN~" < /etc/prometheus/prometheus.yml.tpl > /etc/prometheus/prometheus.yml

exec /bin/prometheus "$@"
