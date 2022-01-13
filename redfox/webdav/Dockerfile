FROM alpine
RUN wget -O /caddy 'https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fmholt%2Fcaddy-webdav'
COPY Caddyfile /Caddyfile
EXPOSE 80 443
ENTRYPOINT [ "/caddy" ]
