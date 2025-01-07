#!/bin/sh
set -ex
rm -f /tmp/minecraft-fifo
mkfifo /tmp/minecraft-fifo
cat /tmp/minecraft-fifo | java -Xmx8G -Xms8G -Djline.terminal=jline.UnsupportedTerminal -jar server.jar nogui
