FROM hranicky/fitcrack_server:2.4.0

RUN apt-get -y update && apt-get -y install certbot

COPY entrypoint.sh /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]