#!/bin/sh

# certbot certonly --non-interactive --agree-tos -m ssl@foxden.network -d auth.foxden.network --standalone

while :; do
    certbot renew --cron --non-interactive
    sleep 24h
done
