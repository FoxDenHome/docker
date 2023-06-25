FROM ghcr.io/akpw/mktxp:latest

COPY mktxp.conf /home/mktxp/mktxp/mktxp.conf.tpl
RUN envsubst < /home/mktxp/mktxp/mktxp.conf.tpl > /home/mktxp/mktxp/mktxp.conf
