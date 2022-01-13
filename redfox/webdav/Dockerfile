FROM alpine
RUN apk --no-cache add envsubst
RUN wget -O /caddy 'https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fmholt%2Fcaddy-webdav' && chmod +x /caddy
COPY Caddyfile /Caddyfile.tpl
COPY run.sh /run.sh
EXPOSE 80 443
ENTRYPOINT [ "/run.sh" ]
