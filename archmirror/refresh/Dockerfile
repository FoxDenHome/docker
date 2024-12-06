FROM alpine:3.21

RUN apk add bash rsync curl

COPY *.sh /

ENTRYPOINT [ "/loop.sh" ]
