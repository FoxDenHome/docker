FROM alpine AS builder
RUN wget -O - 'https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fmholt%2Fcaddy-webdav' | tar xz caddy

FROM alpine
COPY --from=builder caddy /caddy
COPY Caddyfile /Caddyfile
EXPOSE 80 443
ENTRYPOINT [ "caddy" ]
