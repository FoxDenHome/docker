FROM telegraf:latest

RUN echo "deb http://ftp.us.debian.org/debian bookworm main non-free" >> /etc/apt/sources.list && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends iputils-ping snmp procps snmp-mibs-downloader && \
    rm -rf /var/lib/apt/lists/*

COPY conf/ /etc/telegraf/
COPY mibs/ /var/lib/mibs/ietf/
