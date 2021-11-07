FROM prom/prometheus:latest

COPY prometheus.yml /etc/prometheus/prometheus.yml.tpl
COPY preproc.sh /prometheus-preproc.sh

ENTRYPOINT [ "/prometheus-preproc.sh" ]
