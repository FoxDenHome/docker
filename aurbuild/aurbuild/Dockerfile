FROM ghcr.io/doridian/aurbuild/aurbuild:latest

COPY packages.txt /aur/packages.txt

RUN pacman -Syu --noconfirm --needed \
            # Below here should be in PKGBUILD but isnt \
            libxkbcommon \
            libcanberra \
            gst-plugins-bad
