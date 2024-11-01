FROM alpine:3.20

RUN apk add bash rsync curl

COPY *.sh /

ENTRYPOINT [ "/loop.sh" ]
