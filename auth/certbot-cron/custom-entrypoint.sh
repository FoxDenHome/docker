#!/bin/sh

# certbot certonly --non-interactive --agree-tos -m ssl@foxden.network -d auth.foxden.network --standalone

while :; do
    certbot renew --non-interactive
    chown -R 1000:1000 /etc/letsencrypt
    sleep 24h
done
