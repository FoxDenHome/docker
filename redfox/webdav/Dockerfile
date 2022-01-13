FROM alpine AS builder
RUN wget -O - 'https://caddyserver.com/download/linux/amd64?plugins=http.webdav&license=personal&telemetry=off' | tar xz caddy

FROM alpine
COPY --from=builder caddy /caddy
COPY Caddyfile /Caddyfile
EXPOSE 80 443
ENTRYPOINT [ "caddy" ]
