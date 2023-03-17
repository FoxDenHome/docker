FROM caddy:latest-builder AS builder

RUN xcaddy build \
    --with github.com/mastercactapus/caddy2-proxyprotocol

FROM caddy:latest

USER root
COPY --from=builder /usr/bin/caddy /usr/bin/caddy

ENV PUID=10000
ENV PGID=10000

RUN apk add --no-cache curl s6 python3 samba-client

RUN adduser -D -s "/bin/nologin" -u 11000 smbauth

COPY etc/ /etc/

ENTRYPOINT [ "s6-svscan", "/etc/s6" ]
