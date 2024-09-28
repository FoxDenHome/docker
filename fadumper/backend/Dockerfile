FROM ghcr.io/doridian/fadumper/backend:latest

RUN apk --no-cache add openssh

RUN adduser -u 989 -g 989 -D -s /bin/false proxyuser

RUN mkdir -p /home/proxyuser/.ssh && \
        ssh-keyscan -H icefox.doridian.net > /home/proxyuser/.ssh/known_hosts & \
        chown -R proxyuser:proxyuser /home/proxyuser/.ssh

COPY etc /etc
