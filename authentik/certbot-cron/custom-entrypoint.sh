#!/bin/sh

# certbot certonly --non-interactive --agree-tos -m ssl@foxden.network -d auth.foxden.network --standalone

while :; do
    certbot renew --non-interactive
    sleep 24h
done
