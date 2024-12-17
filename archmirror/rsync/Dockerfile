FROM debian:bookworm-slim

RUN apt-get update -y && apt-get install --no-install-recommends -y rsync netcat-traditional && apt-get clean

COPY rsyncd.conf /etc/rsyncd.conf
ENTRYPOINT [ "rsync", "--daemon", "--no-detach" ]
