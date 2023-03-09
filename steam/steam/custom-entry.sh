#!/bin/bash -e

/usr/local/bin/modemgr --defaults

if [ ! -z "$DEFAULT_SIZEW" ]
then
    /usr/local/bin/modemgr --switch -x $DEFAULT_SIZEW -y $DEFAULT_SIZEH -r $DEFAULT_REFRESH
fi

exec $KDE_START
