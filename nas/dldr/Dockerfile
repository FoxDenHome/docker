FROM binhex/arch-delugevpn:latest


RUN sed -i 's:sysctl -q net.ipv4.conf.all.src_valid_mark=1:echo skipping setting net.ipv4.conf.all.src_valid_mark:' /usr/bin/wg-quick
RUN echo 'ip link set wg0 mtu 1420' >> /root/wireguardup.sh

RUN sed -i 's:incoming_ports_lan_array=():incoming_ports_lan_array=(9100):' /root/iptable.sh
RUN rm -f /usr/sbin/ip6tables && ln -sf /bin/true /usr/sbin/ip6tables

COPY config_deluge_type.py /config_deluge_type.py
RUN chown 0:0 /config_deluge_type.py && chmod 755 /config_deluge_type.py && \
        cat /home/nobody/config_deluge.py >> /config_deluge_type.py

RUN sed -i 's:rm -f /config/deluged.pid:rm -f /config/deluged.pid ; /deluge_config.sh:' /home/nobody/deluge.sh

COPY deluge_config.sh /deluge_config.sh
RUN chown 0:0 /deluge_config.sh && chmod 755 /deluge_config.sh

RUN curl -vf "https://github.com/joelacus/deluge-web-dark-theme/raw/8d44250edbd193719aa57a65fd39c2d706d2e66f/deluge_web_dark_theme.tar.gz" | \
        tar -xz -C /usr/lib/python3/dist-packages/deluge/ui/web/

RUN mkdir -p /plugins
RUN git clone https://github.com/petroid/Deluge-Pieces-Plugin /tmp/dpp && \
    cd /tmp/dpp && \
    git checkout a9dfb9e270109edb97e5a4c85d4d634c2c3c0bd8 && \
    python setup.py bdist_egg && \
    cp dist/*.egg /plugins/
