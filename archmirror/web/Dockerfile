FROM caddy:latest

ENV PUID=10000
ENV PGID=10000
ENV NAS_WEB_DOMAIN=localhost

RUN apk add --no-cache curl s6

RUN mkdir -p /mnt/archmirror

COPY etc/ /etc/

ENTRYPOINT [ "s6-svscan", "/etc/s6" ]
