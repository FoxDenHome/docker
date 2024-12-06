FROM alpine:3.21

RUN apk add rsync

COPY rsyncd.conf /etc/rsyncd.conf
ENTRYPOINT [ "rsync", "--daemon", "--no-detach" ]
