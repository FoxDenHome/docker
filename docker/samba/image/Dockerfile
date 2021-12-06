FROM debian:stable-slim

RUN apt update && apt -y --no-install-recommends install samba smbclient s6 ethtool nginx avahi-daemon openssh-server python3 zsh samba-vfs-modules

RUN rm -f /etc/ssh/ssh_host_* && ln -sf /var/lib/samba/sshkeys /etc/ssh/hostkeys

RUN sed -i 's~#enable-dbus=yes~enable-dbus=no~' /etc/avahi/avahi-daemon.conf

RUN rm -f /etc/avahi/services/*
COPY etc /etc

RUN mkdir -p /etc/ssh/keys && \
        curl https://raw.githubusercontent.com/Doridian/home-scripts/master/sshkeys/doridian > /etc/ssh/keys/doridian \
        curl https://raw.githubusercontent.com/Doridian/home-scripts/master/sshkeys/wizzy > /etc/ssh/keys/wizzy

RUN /etc/create-users.sh && rm -f /etc/create-users.sh

VOLUME /var/lib/samba

RUN mkdir -p /mnt/nas

ENTRYPOINT ["s6-svscan", "/etc/s6"]
