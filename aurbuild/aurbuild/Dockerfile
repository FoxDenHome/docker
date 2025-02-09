FROM ghcr.io/doridian/aurbuild/aurbuild:latest

RUN pacman -Syu --noconfirm --needed \
            # Below here should be in PKGBUILD but isnt \
            libxkbcommon \
            libcanberra \
            gst-plugins-bad \
            pcsclite \
            ccid \
            yubikey-manager \
            nano

ENV GPG_KEY_ID=723AB072D36DF76677DA5ACF41ADC5FF876838A8

RUN pacman-key --init && \
    pacman-key --recv-key "${GPG_KEY_ID}" && \
    pacman-key --lsign-key "${GPG_KEY_ID}"

USER aur
RUN gpg --recv-keys 6224F9941A8AA6D1 C85668DF69375001 4A2B758631E1FD91 6AD860EED4598027 "${GPG_KEY_ID}"
COPY scdaemon.conf /home/aur/.gnupg/scdaemon.conf

USER root
COPY packages.txt /aur/packages.txt
