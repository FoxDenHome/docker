#!/bin/bash -e

export PATH="${PATH}:/usr/local/games:/usr/games"
export LD_LIBRARY_PATH="/usr/lib/libreoffice/program:${LD_LIBRARY_PATH}"
export DISPLAY=":0"

/usr/local/bin/modemgr --defaults

if [ ! -z "$DEFAULT_SIZEW" ]
then
    /usr/local/bin/modemgr --switch -x $DEFAULT_SIZEW -y $DEFAULT_SIZEH -r $DEFAULT_REFRESH
fi

exec startplasma-x11
