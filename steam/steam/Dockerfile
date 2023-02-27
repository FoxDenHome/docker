FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root

RUN adduser user render
RUN groupmod -o -g 107 input
RUN add-apt-repository -y ppa:ar-lex/gamescope

RUN apt update && \
        apt -y dist-upgrade && \
        wget https://github.com/LizardByte/Sunshine/releases/download/v0.18.4/sunshine-ubuntu-22.04-amd64.deb -O /tmp/sunshine.deb && \
        apt -y install steam pipewire pipewire-audio-client-libraries libspa-0.2-bluetooth libspa-0.2-jack wireplumber gamescope /tmp/sunshine.deb zsh && \
        rm -f /tmp/sunshine.deb && \
        usermod -s /bin/zsh user

COPY custom-entry.sh /etc/custom-entry.sh
RUN chown root:root /etc/custom-entry.sh && chmod 755 /etc/custom-entry.sh
# RUN sed 's~export DISPLAY=":0"~. /etc/custom-entry.sh~' -i /etc/entrypoint.sh

# COPY supervisord.conf /etc/supervisord.conf

RUN rm -f /usr/lib/x86_64-linux-gnu/wireplumber-0.4/libwireplumber-module-logind.so

# ENV PULSE_SERVER=unix:/tmp/runtime-user/pulse/native
# ENV DISPLAY=
ENV SEATD_VTBOUND=0
ENV WLR_LIBINPUT_NO_DEVICES=1

USER user
