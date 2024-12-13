FROM debian:bookworm-slim

RUN apt-get update -y && apt-get install -y rsync && apt-get clean

COPY rsyncd.conf /etc/rsyncd.conf
ENTRYPOINT [ "rsync", "--daemon", "--no-detach" ]
