#!/bin/sh
set -e

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

iptables -F
ip6tables -F

iptables -N LOGDROP || true
#iptables -A LOGDROP -j LOG
iptables -A LOGDROP -j DROP

iptables -N BROADCAST || true
iptables -A BROADCAST -m physdev --physdev-in wlan0 -p udp --sport 68 --dport 67 -j ACCEPT
iptables -A BROADCAST -m physdev --physdev-in eth0.5 -p udp --sport 67 --dport 68 -j ACCEPT
iptables -A BROADCAST -j LOGDROP

iptables -A INPUT -i wlan0 -j LOGDROP
iptables -A INPUT -i eth0.5 -j LOGDROP
iptables -A INPUT -i br0 -j LOGDROP
iptables -P FORWARD DROP
iptables -A FORWARD -d 255.255.255.255 -j BROADCAST
iptables -A FORWARD -m physdev --physdev-in wlan0 --physdev-out wlan0 -j LOGDROP
iptables -A FORWARD -m physdev --physdev-in eth0.5 -j ACCEPT
iptables -A FORWARD -d 192.168.5.5 -j ACCEPT
iptables -A FORWARD -d 192.168.5.0/24 -j LOGDROP
iptables -A FORWARD ! -s 192.168.5.0/24 -j LOGDROP
iptables -A FORWARD -m physdev --physdev-is-bridged -j ACCEPT
iptables -A FORWARD -j LOGDROP
ip6tables -A INPUT -i wlan0 -j REJECT
ip6tables -A INPUT -i eth0.5 -j REJECT
ip6tables -A INPUT -i br0 -j REJECT
ip6tables -P FORWARD DROP

echo 0 > /proc/sys/net/ipv6/conf/br0/accept_ra
echo 0 > /proc/sys/net/ipv6/conf/eth0.5/accept_ra
echo 2 > /proc/sys/net/ipv6/conf/eth0/accept_ra

/etc/init.d/hostapd start

