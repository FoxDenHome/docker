FROM amazoncorretto:8

USER root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /data
USER 1000:1000
ENTRYPOINT [ "/entrypoint.sh" ]
