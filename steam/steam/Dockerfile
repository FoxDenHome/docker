FROM josh5/steam-headless:latest

RUN touch /tmp/.udev-started
RUN sed 's~/usr/bin/x11vnc~/usr/bin/x11vnc -noshm~' -i /usr/bin/start-x11vnc.sh
