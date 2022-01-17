FROM alpine:latest

RUN apk add --no-cache ca-certificates wget curl s6 openssh-server zsh

RUN rm -f /etc/ssh/ssh_host_*

COPY etc /etc

RUN mkdir -p /etc/ssh/keys
RUN /etc/create-users.sh && rm -f /etc/create-users.sh

VOLUME /etc/ssh/hostkeys

ENTRYPOINT ["/etc/run.sh"]
