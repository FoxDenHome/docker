FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root

RUN adduser user render
RUN add-apt-repository -y ppa:ar-lex/gamescope

RUN apt update && \
        apt -y dist-upgrade && \
        wget https://github.com/LizardByte/Sunshine/releases/download/v0.18.4/sunshine-ubuntu-22.04-amd64.deb -O /tmp/sunshine.deb && \
        apt -y install steam pipewire gamescope /tmp/sunshine.deb && \
        rm -f /tmp/sunshine.deb

COPY custom-entry.sh /etc/custom-entry.sh
RUN chown root:root /etc/custom-entry.sh && chmod 755 /etc/custom-entry.sh
RUN sed 's~export DISPLAY=":0"~. /etc/custom-entry.sh~' -i /etc/entrypoint.sh

USER user
