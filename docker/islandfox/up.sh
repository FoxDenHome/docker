#!/bin/sh
docker-compose -f networks.yml -f monitoring.yml -f mdns-repeater.yml up -d
