FROM caddy:builder AS builder

RUN xcaddy build \
    --with github.com/mholt/caddy-webdav

FROM caddy:latest

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

COPY Caddyfile.tpl /etc/caddy/Caddyfile.tpl

COPY startup.sh /startup.sh
ENTRYPOINT [ "/startup.sh" ]
