FROM koush/scrypted:latest

RUN apt update && apt -y install avahi-daemon && rm /etc/avahi/services/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

CMD ["/entrypoint.sh"]
