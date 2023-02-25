FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root
RUN apt update && apt -y dist-upgrade && apt -y install steam
RUN wget https://github.com/LizardByte/Sunshine/releases/download/v0.18.4/sunshine-ubuntu-22.04-amd64.deb -O /tmp/sunshine.deb && apt -y install /tmp/sunshine.deb && rm -f /tmp/sunshine.deb
USER user
