#!/bin/bash -e

/usr/local/bin/modemgr.py --defaults

exec $KDE_START
