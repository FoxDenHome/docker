FROM prom/prometheus:latest

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gettext-base && \
    rm -rf /var/lib/apt/lists/*

COPY prometheus.yml /etc/prometheus/prometheus.yml.tpl
COPY preproc.sh /prometheus-preproc.sh

ENTRYPOINT [ "/prometheus-preproc.sh" ]
