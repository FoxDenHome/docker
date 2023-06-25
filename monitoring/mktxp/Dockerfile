FROM ghcr.io/akpw/mktxp:latest

COPY --chmod=755 entrypoint.sh /entrypoint.sh
COPY mktxp.conf /home/mktxp/mktxp/mktxp.conf.tpl

USER root
RUN chown -R mktxp:mktxp /home/mktxp
USER mktxp

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
