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
        isolate_host \
        compat_roles \
        discoitems \
        sasl2 \
        sasl_ssdp \
        bind2 \
 && apt-get update \
 && apt-get install -y --no-install-recommends lua-luaossl \
 && rm -rf '/usr/src/prosody-modules' '/usr/local/lib/prosody/custom-modules/mod_bookmarks.lua'

COPY s6 /etc/s6
RUN rm -rf /usr/local/etc/prosody
COPY conf /usr/local/etc/prosody
RUN mkdir -p /usr/local/etc/prosody/certs

ENTRYPOINT [ "/usr/bin/s6-svscan", "/etc/s6" ]
