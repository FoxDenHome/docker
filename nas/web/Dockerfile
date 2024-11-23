FROM caddy:builder AS builder

RUN xcaddy build \
    --with github.com/mholt/caddy-webdav

FROM caddy:latest

USER root
COPY --from=builder /usr/bin/caddy /usr/bin/caddy

ENV NAS_WEB_DOMAIN=localhost

RUN mkdir -p /mnt/archmirror

COPY etc/ /etc/
