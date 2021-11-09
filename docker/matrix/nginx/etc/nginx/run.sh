#!/bin/sh
(
    while :
    do
        sleep 6h
        nginx -s reload
    done
) &
nginx -g 'daemon off;'
