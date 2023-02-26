FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root

RUN adduser user render
RUN add-apt-repository -y ppa:ar-lex/gamescope

ENV PULSE_SERVER unix:/tmp/runtime-user/pulse/native

RUN apt update && \
        apt -y dist-upgrade && \
        wget https://github.com/LizardByte/Sunshine/releases/download/v0.18.4/sunshine-ubuntu-22.04-amd64.deb -O /tmp/sunshine.deb && \
        apt -y install steam pipewire pipewire-audio-client-libraries libspa-0.2-bluetooth libspa-0.2-jack wireplumber gamescope /tmp/sunshine.deb && \
        rm -f /tmp/sunshine.deb

#COPY custom-entry.sh /etc/custom-entry.sh
#RUN chown root:root /etc/custom-entry.sh && chmod 755 /etc/custom-entry.sh
#RUN sed 's~# Add custom processes right below this line, or within `supervisord.conf` to perform service management similar to systemd~. /etc/custom-entry.sh~' -i /etc/entrypoint.sh

COPY supervisord.conf /etc/supervisord.conf

USER user
