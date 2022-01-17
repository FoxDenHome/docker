FROM alpine:latest

RUN apk add --no-cache ca-certificates samba s6 avahi

RUN sed -i 's~#enable-dbus=yes~enable-dbus=no~' /etc/avahi/avahi-daemon.conf

RUN rm -f /etc/avahi/services/*
COPY etc /etc

RUN /etc/create-users.sh && rm -f /etc/create-users.sh

VOLUME /var/lib/samba

ENTRYPOINT ["s6-svscan", "/etc/s6"]
