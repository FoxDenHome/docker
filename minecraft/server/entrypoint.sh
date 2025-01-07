#!/bin/sh
java -Xmx8G -Xms8G -Djline.terminal=jline.UnsupportedTerminal -jar server.jar nogui < /dev/null
