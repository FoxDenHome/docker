FROM binhex/arch-delugevpn:latest

RUN sed -i 's:sysctl -q net.ipv4.conf.all.src_valid_mark=1:echo skipping setting net.ipv4.conf.all.src_valid_mark:' /usr/bin/wg-quick
