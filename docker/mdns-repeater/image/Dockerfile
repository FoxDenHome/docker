FROM alpine:latest AS builder
ARG MDNS_REPEATER_VERSION=local

RUN apk add build-base libcap

ADD mdns-repeater.c mdns-repeater.c

RUN gcc -static -O2 -o /bin/mdns-repeater mdns-repeater.c -DMDNS_REPEATER_VERSION=\"${MDNS_REPEATER_VERSION}\" && strip /bin/mdns-repeater
RUN chown root:root /bin/mdns-repeater && chmod 0755 /bin/mdns-repeater && setcap cap_net_raw=+ep /bin/mdns-repeater

FROM scratch

COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder /bin/mdns-repeater /bin/mdns-repeater

USER daemon

ENTRYPOINT ["/bin/mdns-repeater", "-f"]
CMD ["eth0", "docker0"]
