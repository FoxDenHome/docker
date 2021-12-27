#!/bin/sh
set -e

echo '*/5 * * * * root /opt/home-scripts/docker/_nvidia/checker.py' > /etc/cron.d/home-scripts-nvidia-checker
systemctl restart cron
