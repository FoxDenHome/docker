FROM alpine

ENV CGO_ENABLED 0
ARG REST_SERVER_VERSION=0.13.0

RUN mkdir -p /tmp/dl && \
    wget https://github.com/restic/rest-server/releases/download/v${REST_SERVER_VERSION}/rest-server_${REST_SERVER_VERSION}_linux_amd64.tar.gz -O /tmp/dl/rest-server.tar.gz && \
    tar -xvf /tmp/dl/rest-server.tar.gz && \
    mv /tmp/dl/*/rest-server /rest-server

ENTRYPOINT [ "/rest-server", "--path", "/data", "--private-repos" ]
