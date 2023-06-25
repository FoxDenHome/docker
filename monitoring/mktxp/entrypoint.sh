#!/bin/sh
set -e

envsubst < /home/mktxp/mktxp/mktxp.conf.tpl > /home/mktxp/mktxp/mktxp.conf

exec /usr/local/bin/mktxp export
