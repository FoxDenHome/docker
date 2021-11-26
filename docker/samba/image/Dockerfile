FROM debian:stable-slim

RUN apt update && apt -y --no-install-recommends install samba s6 ethtool nginx avahi openssh python3 zsh

RUN rm -f /etc/ssh/ssh_host_* && ln -sf /var/lib/samba/sshkeys /etc/ssh/hostkeys

RUN sed -i 's~#enable-dbus=yes~enable-dbus=no~' /etc/avahi/avahi-daemon.conf

RUN rm -f /etc/avahi/services/*
COPY etc /etc

RUN /etc/create-users.sh && rm -f /etc/create-users.sh

VOLUME /var/lib/samba

RUN mkdir -p /mnt/nas

ENTRYPOINT ["s6-svscan", "/etc/s6"]
