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
        git checkout 34df132832847957345e808e7612a05fd2488c33 && \
        git submodule update --init --recursive && \
        npm install && \
        mkdir build && \
        cd build && \
        cmake .. && \
        make -j$(nproc) && \
        cpack -G DEB

COPY apps /home/user/apps
RUN chown -R user:user /home/user/apps
RUN gcc -o /home/user/apps/entry /home/user/apps/entry.c
RUN gcc -o /home/user/apps/wait-for-x11 /home/user/apps/wait-for-x11.c
RUN gcc -o /home/user/apps/nvidia-monitor /home/user/apps/nvidia-monitor.c

FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root

RUN apt -y remove --purge akonadi-server && \
        apt -y --purge autoremove

RUN apt update && \
        apt -y dist-upgrade && \
        apt -y install steam zsh

COPY nvidia-install.sh /etc/nvidia-install.sh
RUN chown root:root /etc/nvidia-install.sh && chmod 755 /etc/nvidia-install.sh
ARG NVIDIA_DRIVER_VERSION
RUN /etc/nvidia-install.sh "${NVIDIA_DRIVER_VERSION}"

RUN adduser user render && \
        groupmod -o -g 107 input && \
        usermod -s /bin/zsh user

COPY --from=builder /home/user/Sunshine/build/cpack_artifacts/Sunshine.deb /tmp/sunshine.deb
RUN apt -y install /tmp/sunshine.deb && \
        rm -f /tmp/sunshine.deb

ENV DEFAULT_SIZEW=
ENV DEFAULT_SIZEH=
ENV DEFAULT_REFRESH=

COPY custom-entry.sh /etc/custom-entry.sh
RUN chown root:root /etc/custom-entry.sh && chmod 755 /etc/custom-entry.sh
COPY kill-all.sh /etc/kill-all.sh
RUN chown root:root /etc/kill-all.sh && chmod 755 /etc/kill-all.sh
COPY modemgr.py /usr/local/bin/modemgr
RUN chown root:root /usr/local/bin/modemgr && chmod 755 /usr/local/bin/modemgr

RUN sed 's~sudo nvidia-xconfig~sudo nvidia-xconfig --cool-bits=28~' -i /etc/entrypoint.sh
RUN sed 's~$KDE_START &~. /etc/custom-entry.sh~' -i /etc/entrypoint.sh
RUN sed 's~exit 1~/etc/kill-all.sh~g' -i /etc/entrypoint.sh
RUN sed 's~if ! command -v nvidia-xconfig &> /dev/null; then~if ! /etc/nvidia-install.sh "\$(head -n1 </proc/driver/nvidia/version | awk \'\{print \$8\}\')"; then~g' -i /etc/entrypoint.sh
COPY supervisord.conf /etc/supervisord.conf

RUN sed 's~selkies-gstreamer~exec selkies-gstreamer~g' -i /etc/selkies-gstreamer-entrypoint.sh

COPY --from=builder /home/user/apps /apps
RUN chown root:root /apps/* && chmod 755 /apps/* && chmod +s /apps/entry

USER user
ENTRYPOINT [ "/apps/entry" ]
