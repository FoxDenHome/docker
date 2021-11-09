#!/bin/sh
set -euo pipefail

echo "# Cloudflare IPs" > /etc/nginx/cfips.conf

for ip in `curl https://www.cloudflare.com/ips-v4`
do
    echo "set_real_ip_from $ip;" >> /etc/nginx/cfips.conf
done

for ip in `curl https://www.cloudflare.com/ips-v6`
do
    echo "set_real_ip_from $ip;" >> /etc/nginx/cfips.conf
done
