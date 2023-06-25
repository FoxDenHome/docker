FROM ghcr.io/akpw/mktxp:latest

USER root
RUN apk add --no-cache envsubst
RUN chown -R mktxp:mktxp /home/mktxp
USER mktxp

COPY --chmod=755 entrypoint.sh /entrypoint.sh
COPY mktxp.conf /home/mktxp/mktxp/mktxp.conf.tpl

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
