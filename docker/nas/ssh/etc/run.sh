#!/bin/sh

mkdir -p /etc/ssh/hostkeys
if [ ! -f /etc/ssh/hostkeys/ssh_host_ed25519_key ]
then
    ssh-keygen -A
    mv /etc/ssh/ssh_host_*_key* /etc/ssh/hostkeys/
fi

mkdir -p /run/sshd
chmod +t /run/sshd

exec /usr/sbin/sshd -D -e
