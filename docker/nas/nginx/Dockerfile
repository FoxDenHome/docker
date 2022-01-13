FROM alpine:latest

RUN apk add --no-cache nginx s6 python3 certbot certbot-nginx samba-client

COPY etc /etc

ENTRYPOINT ["s6-svscan", "/etc/s6"]
