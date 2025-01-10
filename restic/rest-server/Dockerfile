FROM alpine

ARG REST_SERVER_VERSION=0.13.0

RUN mkdir -p /tmp/dl && cd /tmp/dl && \
    wget https://github.com/restic/rest-server/releases/download/v${REST_SERVER_VERSION}/rest-server_${REST_SERVER_VERSION}_linux_amd64.tar.gz -O rest-server.tar.gz && \
    tar -xvf rest-server.tar.gz && \
    mv */rest-server /rest-server && \
    cd / && rm -rf /tmp/dl

ENTRYPOINT [ "/rest-server", "--path", "/data", "--private-repos" ]
