#!/bin/sh
set -e

envsubst < /etc/prometheus/prometheus.yml.tpl > /etc/prometheus/prometheus.yml

exec /bin/prometheus "$@"
