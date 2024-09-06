FROM docker.io/kanidm/server:latest

COPY server.toml /etc/kanidm/server.toml

HEALTHCHECK \
    --interval=60s \
    --timeout=10s \
    --start-period=60s \
    --start-interval=5s \
    --retries=3 \
    CMD [ "/sbin/kanidmd", "healthcheck", "-c", "/etc/kanidm/server.toml"]

CMD [ "/sbin/kanidmd", "server", "-c", "/etc/kanidm/server.toml"]
