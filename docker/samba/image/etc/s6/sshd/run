#!/bin/sh

mkdir -p /var/lib/samba/sshkeys
if [ ! -f /var/lib/samba/sshkeys/ssh_host_ed25519_key ]
then
    ssh-keygen -A
    mv /etc/ssh/ssh_host_*_key* /var/lib/samba/sshkeys/
fi

mkdir -p /run/sshd
chmod +t /run/sshd

exec /usr/sbin/sshd -D -e
