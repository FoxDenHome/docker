FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest AS builder

RUN sudo apt-get update && sudo apt-get -y install \
        git \
        build-essential \
        cmake \
        libavdevice-dev \
        libboost-filesystem-dev \
        libboost-log-dev \
        libboost-thread-dev \
        libboost-program-options-dev \
        libboost-locale-dev \
        libcap-dev \
        libdrm-dev \
        libevdev-dev \
        libmfx-dev \
        libnuma-dev \
        libopus-dev \
        libpulse-dev \
        libssl-dev \
        libwayland-dev \
        libx11-dev \
        libxcb-shm0-dev \
        libxcb-xfixes0-dev \
        libxcb-xtest0-dev \
        libxcb1-dev \
        libxfixes-dev \
        libxrandr-dev \
        libxtst-dev \
        nodejs \
        npm \
        nvidia-cuda-dev \
        nvidia-cuda-toolkit \
        libcurl4-openssl-dev \
        libva-dev \
        libvdpau-dev \
        wget

RUN git clone https://github.com/Doridian/Sunshine && \
        cd Sunshine && \
        git checkout 40934fed7d68541cdf60e8d22f50a1cd3ed75dc9 && \
        git submodule update --init --recursive && \
        npm install && \
        mkdir build && \
        cd build && \
        cmake .. && \
        make -j$(nproc) && \
        cpack -G DEB

COPY entry.c /home/user/entry.c
RUN gcc -o /home/user/entry /home/user/entry.c

FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root

RUN apt update && \
        apt -y dist-upgrade && \
        apt -y install steam zsh

RUN adduser user render && \
        groupmod -o -g 107 input && \
        usermod -s /bin/zsh user

COPY --from=builder /home/user/Sunshine/build/cpack_artifacts/Sunshine.deb /tmp/sunshine.deb
RUN apt -y install /tmp/sunshine.deb && \
        rm -f /tmp/sunshine.deb

COPY custom-entry.sh /etc/custom-entry.sh
RUN chown root:root /etc/custom-entry.sh && chmod 755 /etc/custom-entry.sh
COPY kill-all.sh /etc/kill-all.sh
RUN chown root:root /etc/kill-all.sh && chmod 755 /etc/kill-all.sh
COPY modemgr.py /usr/local/bin/modemgr.py
RUN chown root:root /usr/local/bin/modemgr.py && chmod 755 /usr/local/bin/modemgr.py

RUN sed 's~sudo nvidia-xconfig~sudo nvidia-xconfig --cool-bits=28~' -i /etc/entrypoint.sh
RUN sed 's~$KDE_START &~. /etc/custom-entry.sh~' -i /etc/entrypoint.sh
RUN sed 's~exit 1~/etc/kill-all.sh~g' -i /etc/entrypoint.sh
COPY supervisord.conf /etc/supervisord.conf

RUN sed 's~selkies-gstreamer~exec selkies-gstreamer~g' -i /etc/selkies-gstreamer-entrypoint.sh

COPY --from=builder /home/user/entry /entry
RUN chown root:root /entry && chmod 755 /entry && chmod +s /entry

USER user
ENTRYPOINT [ "/entry" ]
