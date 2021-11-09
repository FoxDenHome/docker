#!/bin/sh
(
    while :
    do
        sleep 6h
        nginx -s reload
    done
) &
nginx -c /etc/nginx/nginx.conf -g 'daemon off;'
