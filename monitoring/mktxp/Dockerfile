FROM ghcr.io/akpw/mktxp:latest

RUN mkdir -p /home/mktxp/mktxp

COPY --chmod=755 entrypoint.sh /entrypoint.sh
COPY mktxp.conf /home/mktxp/mktxp/mktxp.conf.tpl

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
