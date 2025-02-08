FROM ghcr.io/doridian/aurbuild/aurbuild:latest

RUN pacman -Syu --noconfirm --needed \
            # Below here should be in PKGBUILD but isnt \
            libxkbcommon \
            libcanberra \
            gst-plugins-bad

ENV HOME=/root
RUN gpg --recv-keys 6224F9941A8AA6D1 C85668DF69375001 4A2B758631E1FD91 723AB072D36DF76677DA5ACF41ADC5FF876838A8 && \
    pacman-key --init && \
    pacman-key --recv-key 723AB072D36DF76677DA5ACF41ADC5FF876838A8 && \
    pacman-key --lsign-key 723AB072D36DF76677DA5ACF41ADC5FF876838A8

ENV HOME=/home/aur
RUN gpg --recv-keys 6224F9941A8AA6D1 C85668DF69375001 4A2B758631E1FD91 723AB072D36DF76677DA5ACF41ADC5FF876838A8

COPY packages.txt /aur/packages.txt
