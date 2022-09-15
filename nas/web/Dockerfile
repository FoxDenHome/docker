FROM caddy:latest

ENV PUID=10000
ENV PGID=10000

USER root

RUN apk add --no-cache curl s6 python3 samba-client

RUN adduser -D -s "/bin/nologin" -u 11000 smbauth

COPY etc/ /etc/

ENTRYPOINT [ "s6-svscan", "/etc/s6" ]
