#!/bin/sh
set -e

cat /home/mktxp/mktxp/mktxp.conf.tpl | sed "s/__MTIK_USERNAME__/${MTIK_USERNAME}/g" | sed "s/__MTIK_PASSWORD__/${MTIK_PASSWORD}/g" > /home/mktxp/mktxp/mktxp.conf

exec /usr/local/bin/mktxp export
