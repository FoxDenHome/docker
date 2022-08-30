FROM binhex/arch-delugevpn:latest

RUN sed -i 's:sysctl -q net.ipv4.conf.all.src_valid_mark=1:echo skipping setting net.ipv4.conf.all.src_valid_mark:' /usr/bin/wg-quick

RUN echo 'ip link set wg0 mtu 1420' >> /root/wireguardup.sh

RUN sed -i 's:incoming_ports_lan_array=():incoming_ports_lan_array=(9100):' /root/iptable.sh
