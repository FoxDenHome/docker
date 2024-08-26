FROM alpine:latest AS mimefix

RUN apk add --no-cache mailcap python3

COPY neuter-mime-types.py /sbin/neuter-mime-types.py
RUN chmod +x /sbin/neuter-mime-types.py && /sbin/neuter-mime-types.py

FROM caddy:latest

# The below ensures Golang cannot find any other MIME database before ours
RUN rm -rf /usr/local/share/mime/globs2 /usr/share/mime/globs2

COPY --from=mimefix /etc/mime.types.neutered /etc/mime.types

COPY etc/ /etc/
