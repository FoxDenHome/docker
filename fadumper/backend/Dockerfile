FROM ghcr.io/doridian/fadumper/backend:latest

RUN apk --no-cache add openssh

RUN adduser -u 989 -g 989 -s /bin/false proxyuser 

COPY etc /etc
