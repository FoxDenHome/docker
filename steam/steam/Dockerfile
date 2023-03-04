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
    nvidia-cuda-toolkit

RUN git clone https://github.com/Doridian/Sunshine && \
        cd Sunshine && \
        git checkout 678a05217e02fbaf7baabebb4025d9ae8b20e8bc && \
        git submodule update --init --recursive && \
        npm install && \
        mkdir build && \
        cd build && \
        cmake .. && \
        make -j$(nproc) && \
        cpack -G DEB

FROM ghcr.io/selkies-project/nvidia-glx-desktop:latest

USER root

RUN apt update && \
        apt -y dist-upgrade && \
        apt -y install steam zsh

RUN adduser user render && \
        groupmod -o -g 107 input && \
        usermod -s /bin/zsh user

COPY --from=builder /home/user/Sunshine/build/cpack_artifacts/Sunshine.dev /tmp/sunshine.deb
RUN apt -y install /tmp/sunshine.deb zsh && \
        rm -f /tmp/sunshine.deb

COPY custom-entry.sh /etc/custom-entry.sh
COPY addmodes.py /etc/addmodes.py
RUN chown root:root /etc/custom-entry.sh && chmod 755 /etc/custom-entry.sh
RUN chown root:root /etc/addmodes.py && chmod 755 /etc/addmodes.py

RUN sed 's~sudo nvidia-xconfig~sudo nvidia-xconfig --cool-bits=28~' -i /etc/entrypoint.sh
RUN sed 's~$KDE_START &~. /etc/custom-entry.sh~' -i /etc/entrypoint.sh
COPY supervisord.conf /etc/supervisord.conf

USER user
