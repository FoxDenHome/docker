FROM alpine:latest

RUN apk add --no-cache nginx s6 certbot certbot-nginx

COPY etc /etc

ENTRYPOINT ["s6-svscan", "/etc/s6"]
