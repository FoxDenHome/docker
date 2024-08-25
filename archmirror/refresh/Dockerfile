FROM alpine:3.20

RUN apk add bash rsync

COPY *.sh /

ENTRYPOINT [ "/loop.sh" ]
