#!/bin/sh
exec java -Xmx8G -Xms8G -Djline.terminal=jline.UnsupportedTerminal -jar server.jar nogui
