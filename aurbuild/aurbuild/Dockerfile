FROM ghcr.io/doridian/aurbuild/aurbuild:latest

RUN pacman -Syu --noconfirm --needed \
            # Below here should be in PKGBUILD but isnt \
            libxkbcommon \
            libcanberra \
            gst-plugins-bad

RUN pacman-key --recv-keys 6224F9941A8AA6D1 && \
    pacman-key --lsign-key 6224F9941A8AA6D1

COPY packages.txt /aur/packages.txt
