#!/bin/sh
docker-compose -f networks.yml -f samba.yml -f foxcaves.yml -f plex.yml -f dldr.yml -f syncthing.yml up -d
