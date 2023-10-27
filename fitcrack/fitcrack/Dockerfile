FROM hranicky/fitcrack_server:2.4.0

RUN apt-get -y update && apt-get -y install certbot cron
RUN rm -rf /srv/certificates && ln -s /etc/letsencrypt /srv/certificates
COPY entrypoint.sh /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]
