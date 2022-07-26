FROM alpine:latest

RUN apk add --no-cache ca-certificates samba s6

COPY etc /etc

RUN /etc/create-users.sh && rm -f /etc/create-users.sh

VOLUME /var/lib/samba

ENTRYPOINT ["s6-svscan", "/etc/s6"]
