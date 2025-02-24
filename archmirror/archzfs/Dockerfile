FROM debian:bookworm-slim

RUN apt-get -y update && apt-get -y install jq curl bash rsync

COPY mirror.sh /mirror.sh
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
