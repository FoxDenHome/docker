FROM binhex/arch-delugevpn:latest

RUN sed -i 's:sysctl -q net.ipv4.conf.all.src_valid_mark=1:echo skipping setting net.ipv4.conf.all.src_valid_mark:' /usr/bin/wg-quick
RUN echo 'ip link set wg0 mtu 1420' >> /root/wireguardup.sh

RUN sed -i 's:incoming_ports_lan_array=():incoming_ports_lan_array=(9100):' /root/iptable.sh
RUN rm -f /usr/sbin/ip6tables && ln -sf /bin/true /usr/sbin/ip6tables

RUN mkdir -p /plugins
RUN git clone https://github.com/nicklan/Deluge-Pieces-Plugin /tmp/dpp && \
    cd /tmp/dpp && \
    python setup.py bdist_egg && \
    cp dist/*.egg /plugins/

CMD ["/bin/bash", "/custom-init.sh"]
