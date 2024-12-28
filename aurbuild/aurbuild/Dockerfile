FROM ghcr.io/doridian/aurbuild/aurbuild:latest

RUN pacman -Syu --noconfirm --needed \
            # Below here should be in PKGBUILD but isnt \
            libxkbcommon \
            libcanberra \
            gst-plugins-bad

ENV HOME=/root
RUN gpg --recv-keys 6224F9941A8AA6D1 C85668DF69375001 && \
    pacman-key --init && \
    pacman-key --recv-key 459B9477FCE9B8CD889DFFC2C55F467DFDC3DFC8 && \
    pacman-key --lsign-key 459B9477FCE9B8CD889DFFC2C55F467DFDC3DFC8

ENV HOME=/home/aur
RUN gpg --recv-keys 6224F9941A8AA6D1 C85668DF69375001

COPY packages.txt /aur/packages.txt
