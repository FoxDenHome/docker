FROM ghcr.io/doridian/fadumper/backend:latest

RUN apk --no-cache add openssh

RUN adduser -u 999 -g 999 -s /bin/false proxyuser 

COPY etc /etc
