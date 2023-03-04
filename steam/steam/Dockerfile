FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root

RUN apt update && \
        apt -y dist-upgrade && \
        apt -y install steam zsh

RUN adduser user render && \
        groupmod -o -g 107 input && \
        usermod -s /bin/zsh user

RUN wget https://github.com/Doridian/Sunshine/releases/download/xinput-dev/sunshine-22.04.deb -O /tmp/sunshine.deb && \
        apt -y install /tmp/sunshine.deb zsh && \
        rm -f /tmp/sunshine.deb

COPY custom-entry.sh /etc/custom-entry.sh
COPY addmodes.py /etc/addmodes.py
RUN chown root:root /etc/custom-entry.sh && chmod 755 /etc/custom-entry.sh
RUN chown root:root /etc/addmodes.py && chmod 755 /etc/addmodes.py

RUN sed 's~sudo nvidia-xconfig~sudo nvidia-xconfig --cool-bits=28~' -i /etc/entrypoint.sh
RUN sed 's~$KDE_START &~. /etc/custom-entry.sh~' -i /etc/entrypoint.sh
COPY supervisord.conf /etc/supervisord.conf

USER user
