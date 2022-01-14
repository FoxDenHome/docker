FROM alpine:latest

RUN apk add --no-cache curl nginx s6 python3 certbot certbot-nginx samba-client

RUN adduser -D -s "/bin/nologin" -u 401 smbauth

COPY etc /etc

ENTRYPOINT ["s6-svscan", "/etc/s6"]
