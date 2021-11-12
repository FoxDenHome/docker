FROM alpine:latest AS builder
ARG MDNS_REPEATER_VERSION=local

RUN apk add build-base libcap

ADD mdns-repeater.c mdns-repeater.c

RUN gcc -static -O2 -o /mdns-repeater mdns-repeater.c -DMDNS_REPEATER_VERSION=\"${MDNS_REPEATER_VERSION}\" && strip /mdns-repeater
RUN chown root:root /mdns-repeater && chmod 0755 /mdns-repeater && setcap cap_net_raw=+ep /mdns-repeater

FROM scratch

COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder /mdns-repeater /mdns-repeater

USER daemon

ENTRYPOINT ["/mdns-repeater"]
CMD ["eth0", "docker0"]
