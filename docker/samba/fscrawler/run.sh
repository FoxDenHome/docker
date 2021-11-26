#!/bin/sh

fscrawler share &
fscrawler homes &

wait -n || exit 1
