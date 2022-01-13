FROM alpine

RUN wget -O /caddy 'https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fmholt%2Fcaddy-webdav' && chmod +x /caddy
COPY Caddyfile /Caddyfile

ENV XDG_DATA_HOME=/data
VOLUME /data

ENV XDG_CONFIG_HOME=/config
VOLUME /config

EXPOSE 80 443

ENTRYPOINT [ "/caddy", "run", "--config", "/Caddyfile" ]
