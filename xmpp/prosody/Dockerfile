FROM sarasmiseth/prosody:latest

USER root
RUN apt-get update && \
        apt-get -y install certbot s6 cron

RUN download-prosody-modules.bash \
 && docker-prosody-module-install.bash \
        cloud_notify \
        cloud_notify_extensions \
        cloud_notify_encrypted \
        cloud_notify_priority_tag \
        cloud_notify_filters \
        privilege \
 && apt-get update \
 && apt-get install -y --no-install-recommends lua-luaossl \
 && rm -rf "/usr/src/prosody-modules"

COPY s6 /etc/s6

ENTRYPOINT [ "/usr/bin/s6-svscan", "/etc/s6" ]
