FROM docker.io/kanidm/server:latest

COPY server.toml /etc/kanidm/server.toml

CMD ["/sbin/kanidmd" "server" "-c" "/etc/kanidm/server.toml"]
