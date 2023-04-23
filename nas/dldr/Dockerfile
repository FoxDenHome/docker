FROM binhex/arch-delugevpn:latest

RUN sed -i 's:sysctl -q net.ipv4.conf.all.src_valid_mark=1:echo skipping setting net.ipv4.conf.all.src_valid_mark:' /usr/bin/wg-quick
RUN echo 'ip link set wg0 mtu 1420' >> /root/wireguardup.sh

RUN sed -i 's:incoming_ports_lan_array=():incoming_ports_lan_array=(9100):' /root/iptable.sh
RUN rm -f /usr/sbin/ip6tables && ln -sf /bin/true /usr/sbin/ip6tables

COPY config_deluge_type.py /config_deluge_type.py
RUN chown 0:0 /config_deluge_type.py && chmod 755 /config_deluge_type.py && \
        cat /home/nobody/config_deluge.py >> /config_deluge_type.py

RUN sed -i 's:rm -f /config/deluged.pid:rm -f /config/deluged.pid && /deluge_config.sh:' /home/nobody/deluge.sh

COPY deluge_config.sh /deluge_config.sh
RUN chown 0:0 /deluge_config.sh && chmod 755 /deluge_config.sh

RUN mkdir -p /plugins
RUN git clone https://github.com/nicklan/Deluge-Pieces-Plugin /tmp/dpp && \
    cd /tmp/dpp && \
    python setup.py bdist_egg && \
    cp dist/*.egg /plugins/
