FROM alpine:3.21

RUN apk --no-cache add jq curl bash rsync

COPY mirror.sh /mirror.sh
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
