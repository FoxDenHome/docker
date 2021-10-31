FROM alpine

RUN apk update && apk add samba s6 ethtool nginx avahi

RUN ln -sf /var/lib/samba/passwd /etc/passwd
RUN ln -sf /var/lib/samba/group /etc/group

COPY etc/s6 /etc/s6

VOLUME /var/lib/samba

RUN mkdir -p /mnt/nas

ENTRYPOINT ["s6-svscan", "/etc/s6"]
